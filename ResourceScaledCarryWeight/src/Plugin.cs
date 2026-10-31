using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Reflection;
using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using UnityEngine;

namespace ResourceScaledCarryWeight
{
    [BepInPlugin(PluginGuid, PluginName, PluginVersion)]
    public sealed class Plugin : BaseUnityPlugin
    {
        public const string PluginGuid = "nikoboi.valheim.resourcescaledcarryweight";
        public const string PluginName = "Resource Scaled Carry Weight";
        public const string PluginVersion = "0.2.0";

        internal static ManualLogSource Log;
        private Harmony _harmony;

        private void Awake()
        {
            Log = Logger;
            _harmony = new Harmony(PluginGuid);

            Patch(typeof(Player), "GetMaxCarryWeight",
                AccessTools.Method(typeof(Patches), nameof(Patches.GetMaxCarryWeightPostfix)));
            Patch(typeof(Game), "UpdateWorldRates",
                AccessTools.Method(typeof(Patches), nameof(Patches.UpdateWorldRatesPostfix)));
            Patch(typeof(ObjectDB), "Awake",
                AccessTools.Method(typeof(Patches), nameof(Patches.ObjectDbAwakePostfix)));

            Logger.LogInfo("Loaded. Carry-weight capacity and all carry-weight status-effect descriptions follow the Resources world rate.");
        }

        private void Patch(Type type, string methodName, MethodInfo postfix)
        {
            MethodInfo target = AccessTools.Method(type, methodName);
            if (target == null)
            {
                Logger.LogError("Could not find " + type.FullName + "." + methodName +
                                ". This game version may have changed its API.");
                return;
            }

            _harmony.Patch(target, postfix: new HarmonyMethod(postfix));
            Logger.LogInfo("Patched " + type.Name + "." + methodName);
        }

        private void OnDestroy()
        {
            _harmony?.UnpatchSelf();
        }
    }

    internal static class Patches
    {
        // Replace the vanilla CarryWeightRate multiplier with ResourceRate while
        // preserving the base value and every status-effect carry-weight bonus.
        internal static void GetMaxCarryWeightPostfix(ref float __result)
        {
            float resourceRate = GameRates.Read("m_resourceRate", 1f);
            float carryWeightRate = GameRates.Read("m_carryWeightRate", 1f);
            if (carryWeightRate <= 0f)
                carryWeightRate = 1f;

            __result *= resourceRate / carryWeightRate;
        }

        internal static void UpdateWorldRatesPostfix()
        {
            TooltipUpdater.Refresh();
        }

        internal static void ObjectDbAwakePostfix()
        {
            TooltipUpdater.Refresh();
        }
    }

    internal static class GameRates
    {
        private static FieldInfo _resourceRateField;
        private static FieldInfo _carryWeightRateField;
        private static bool _lookedUp;

        internal static float Read(string fieldName, float fallback)
        {
            if (!_lookedUp)
            {
                _resourceRateField = AccessTools.Field(typeof(Game), "m_resourceRate");
                _carryWeightRateField = AccessTools.Field(typeof(Game), "m_carryWeightRate");
                _lookedUp = true;

                if (_resourceRateField == null)
                    Plugin.Log.LogError("Game.m_resourceRate was not found; Resource Rate will default to 1.0.");
                if (_carryWeightRateField == null)
                    Plugin.Log.LogWarning("Game.m_carryWeightRate was not found; assuming vanilla CarryWeightRate is 1.0.");
            }

            FieldInfo field = fieldName == "m_resourceRate" ? _resourceRateField : _carryWeightRateField;
            if (field == null || !field.IsStatic)
                return fallback;

            try
            {
                object value = field.GetValue(null);
                return value == null ? fallback : Convert.ToSingle(value, CultureInfo.InvariantCulture);
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("Could not read " + fieldName + ": " + ex.Message);
                return fallback;
            }
        }
    }

    internal static class TooltipUpdater
    {
        private static FieldInfo _statusEffectsField;
        private static FieldInfo _carryBonusField;
        private static FieldInfo _tooltipField;
        private static FieldInfo _itemDescriptionField;
        private static bool _fieldsLookedUp;

        private static readonly Dictionary<StatusEffect, string> OriginalTooltips =
            new Dictionary<StatusEffect, string>();
        private static ItemDrop.ItemData.SharedData _beltSharedData;
        private static string _originalBeltDescription;

        internal static void Refresh()
        {
            if (ObjectDB.instance == null)
                return;

            EnsureFields();
            if (_statusEffectsField == null || _carryBonusField == null || _tooltipField == null)
                return;

            float rate = GameRates.Read("m_resourceRate", 1f);

            try
            {
                RefreshEveryCarryWeightStatusEffect(rate);
                RefreshBeltItem(rate);
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning("Tooltip refresh failed: " + ex);
            }
        }

        private static void EnsureFields()
        {
            if (_fieldsLookedUp)
                return;

            _statusEffectsField = AccessTools.Field(typeof(ObjectDB), "m_StatusEffects");
            _carryBonusField = AccessTools.Field(typeof(SE_Stats), "m_addMaxCarryWeight");
            _tooltipField = AccessTools.Field(typeof(StatusEffect), "m_tooltip");
            _itemDescriptionField = AccessTools.Field(typeof(ItemDrop.ItemData.SharedData), "m_description");
            _fieldsLookedUp = true;

            if (_statusEffectsField == null)
                Plugin.Log.LogError("ObjectDB.m_StatusEffects was not found; cannot enumerate status effects.");
            if (_carryBonusField == null)
                Plugin.Log.LogError("SE_Stats.m_addMaxCarryWeight was not found; cannot identify carry-weight effects.");
            if (_tooltipField == null)
                Plugin.Log.LogError("StatusEffect.m_tooltip was not found; cannot update effect descriptions.");
        }

        private static void RefreshEveryCarryWeightStatusEffect(float rate)
        {
            IEnumerable effects = _statusEffectsField.GetValue(ObjectDB.instance) as IEnumerable;
            if (effects == null)
                return;

            foreach (object entry in effects)
            {
                StatusEffect effect = entry as StatusEffect;
                SE_Stats stats = effect as SE_Stats;
                if (effect == null || stats == null)
                    continue;

                float originalBonus = Convert.ToSingle(_carryBonusField.GetValue(stats), CultureInfo.InvariantCulture);
                if (originalBonus <= 0f)
                    continue;

                if (!OriginalTooltips.ContainsKey(effect))
                    OriginalTooltips.Add(effect, _tooltipField.GetValue(effect) as string);

                string original = OriginalTooltips[effect];
                if (string.IsNullOrEmpty(original))
                    continue;

                float scaledBonus = originalBonus * rate;
                string oldNumber = FormatBonus(originalBonus);
                string newNumber = FormatBonus(scaledBonus);

                // Replace the authored bonus where the game's description includes it.
                // If the source tooltip does not contain the number (for example, a
                // localization token), append an explicit corrected value instead.
                string updated = original.Replace("+" + oldNumber, "+" + newNumber)
                                          .Replace("+ " + oldNumber, "+ " + newNumber);
                if (updated == original)
                    updated = original + "\n\nCarry weight bonus: +" + newNumber + ".";

                _tooltipField.SetValue(effect, updated);
            }
        }

        private static void RefreshBeltItem(float rate)
        {
            GameObject prefab = ObjectDB.instance.GetItemPrefab("BeltStrength");
            if (prefab == null)
                return;

            ItemDrop itemDrop = prefab.GetComponent<ItemDrop>();
            if (itemDrop == null || itemDrop.m_itemData == null || itemDrop.m_itemData.m_shared == null)
                return;

            ItemDrop.ItemData.SharedData shared = itemDrop.m_itemData.m_shared;
            if (_beltSharedData != shared)
            {
                _beltSharedData = shared;
                _originalBeltDescription = _itemDescriptionField == null
                    ? null
                    : _itemDescriptionField.GetValue(shared) as string;
            }

            if (_itemDescriptionField == null || _originalBeltDescription == null)
                return;

            string bonus = FormatBonus(150f * rate);
            _itemDescriptionField.SetValue(shared,
                _originalBeltDescription + "\n\nCarry weight bonus: +" + bonus + ".");
        }

        private static string FormatBonus(float value)
        {
            return value.ToString("0.##", CultureInfo.InvariantCulture);
        }
    }
}

# meal_bank.py  –  Apni Sehat v1.2
# Curated desi meal dataset covering all 6 possible slots.
# Slots: breakfast | snack_am | lunch | snack_pm | dinner | snack_bed
# Tags: desi | veg | high_fiber | low_sodium | low_satfat | light (low carb/cal for SMALL profile)
#
# Pool sizes (prefer_desi=True): breakfast 4, snack_am 4, lunch 6, snack_pm 5, dinner 6, snack_bed 4
# All slots now have >= 4 desi-tagged meals, sufficient to minimise 7-day repeats.

MEALS = [
    # ── BREAKFAST ─────────────────────────────────────────────────────────────
    {
        "name":    "Besan chilla + unsweetened yogurt",
        "name_ur": "بیسن چلہ + بغیر چینی دہی",
        "slot": "breakfast",
        "tags": ["desi", "veg", "high_fiber", "low_satfat", "low_sodium"],
        "carb_servings": 2,
        "notes": "High protein and fibre. Very gentle on blood sugar."
    },
    {
        "name":    "Dalia (cracked wheat) with low-fat milk and almonds",
        "name_ur": "دلیہ (ٹوٹا گندم) کم چکنائی والے دودھ اور بادام کے ساتھ",
        "slot": "breakfast",
        "tags": ["desi", "veg", "high_fiber", "low_sodium"],
        "carb_servings": 2,
        "notes": "No sugar. A few almonds add healthy fat and slow sugar absorption."
    },
    {
        "name":    "2 boiled eggs + 1 slice whole wheat bread + tomato",
        "name_ur": "2 ابلے انڈے + 1 سلائس گندم کی روٹی + ٹماٹر",
        "slot": "breakfast",
        "tags": ["veg", "high_fiber", "low_satfat", "light"],
        "carb_servings": 1,
        "notes": "Boil or poach eggs. Tomato and cucumber on the side."
    },
    {
        "name":    "Oats porridge with chia seeds and walnuts",
        "name_ur": "اوٹس دلیہ چیا سیڈز اور اخروٹ کے ساتھ",
        "slot": "breakfast",
        "tags": ["veg", "high_fiber", "low_sodium", "low_satfat", "light"],
        "carb_servings": 2,
        "notes": "No sugar. Pinch of cinnamon helps blood sugar. Use water or low-fat milk."
    },
    {
        "name":    "1 small whole wheat paratha (minimal oil) + plain yogurt",
        "name_ur": "1 چھوٹا آٹے کا پراٹھا (کم تیل) + سادہ دہی",
        "slot": "breakfast",
        "tags": ["desi", "veg", "low_satfat"],
        "carb_servings": 2,
        "notes": "Very little oil. Yogurt adds protein. No butter or ghee on top."
    },
    {
        "name":    "Moong daal chilla + mint chutney",
        "name_ur": "موں گ دال چلہ + پودینے کی چٹنی",
        "slot": "breakfast",
        "tags": ["desi", "veg", "high_fiber", "low_satfat", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "High protein and fibre. Very gentle on blood sugar."
    },
    {
        "name":    "Anda bhurji (2 eggs) + 1 atta roti",
        "name_ur": "انڈا بھرجی (2 انڈے) + 1 آٹے کی روٹی",
        "slot": "breakfast",
        "tags": ["desi", "low_satfat", "low_sodium"],
        "carb_servings": 1,
        "notes": "Scrambled eggs with tomato, onion, green chilli. Minimal oil."
    },

    # ── MID-MORNING SNACK (snack_am) ──────────────────────────────────────────
    # Small, protein/fibre focused — prevents mid-morning sugar dip
    {
        "name":    "1 boiled egg + cucumber slices",
        "name_ur": "1 ابلا انڈا + کھیرے کی سلائسیں",
        "slot": "snack_am",
        "tags": ["veg", "low_sodium", "light"],
        "carb_servings": 0,
        "notes": "Zero-carb snack — protein keeps you full without spiking sugar."
    },
    {
        "name":    "Small handful of roasted chana (unsalted)",
        "name_ur": "بھنے ہوئے چنے کی مٹھی (بغیر نمک)",
        "slot": "snack_am",
        "tags": ["desi", "veg", "high_fiber", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "High protein and fibre. Roasted, not fried."
    },
    {
        "name":    "Unsweetened yogurt (1 small katori) with flaxseeds",
        "name_ur": "بغیر چینی دہی (1 چھوٹی کٹوری) السی کے ساتھ",
        "slot": "snack_am",
        "tags": ["desi", "veg", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "Probiotic + healthy fat. Flaxseeds add fibre and omega-3."
    },
    {
        "name":    "5 almonds + 1 small guava",
        "name_ur": "5 بادام + 1 چھوٹا امرود",
        "slot": "snack_am",
        "tags": ["veg", "high_fiber", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "Guava is one of the best fruits for diabetics. Almonds slow sugar absorption."
    },
    {
        "name":    "Lassi (salted, low-fat, no sugar)",
        "name_ur": "لسی (نمکین، کم چکنائی، بغیر چینی)",
        "slot": "snack_am",
        "tags": ["desi", "veg", "low_sodium"],
        "carb_servings": 1,
        "notes": "Salted lassi only — no sugar. Cooling and filling."
    },
    {
        "name":    "Akhrot (walnuts) + 1 small apple",
        "name_ur": "اخروٹ + 1 چھوٹا سیب",
        "slot": "snack_am",
        "tags": ["desi", "veg", "high_fiber", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "Walnuts add omega-3 and slow down sugar absorption from the apple."
    },

    # ── LUNCH ─────────────────────────────────────────────────────────────────
    {
        "name":    "Daal maash + 2 atta roti + cucumber salad",
        "name_ur": "دال ماش + 2 آٹے کی روٹیاں + کھیرے کا سلاد",
        "slot": "lunch",
        "tags": ["desi", "veg", "high_fiber", "low_satfat", "low_sodium"],
        "carb_servings": 3,
        "notes": "Legumes lower blood sugar. Keep roti to 1 medium."
    },
    {
        "name":    "Chana curry + 1 atta roti + raita",
        "name_ur": "چنا کری + 1 آٹے کی روٹی + رائتہ",
        "slot": "lunch",
        "tags": ["desi", "veg", "high_fiber"],
        "carb_servings": 3,
        "notes": "Chickpeas are excellent for blood sugar. Avoid too much oil."
    },
    {
        "name":    "Grilled chicken + mixed sabzi + 1 atta roti",
        "name_ur": "گرلڈ چکن + مکس سبزی + 1 آٹے کی روٹی",
        "slot": "lunch",
        "tags": ["desi", "low_satfat", "low_sodium"],
        "carb_servings": 2,
        "notes": "Season with herbs and lemon. No frying."
    },
    {
        "name":    "Mixed vegetable curry + 1 atta roti + plain yogurt",
        "name_ur": "مکس سبزی کری + 1 آٹے کی روٹی + سادہ دہی",
        "slot": "lunch",
        "tags": ["desi", "veg", "low_sodium", "low_satfat", "high_fiber", "light"],
        "carb_servings": 2,
        "notes": "Load up on vegetables. Under 1 tsp oil."
    },
    {
        "name":    "Moong daal soup + 1 atta roti + salad",
        "name_ur": "موں گ دال سوپ + 1 آٹے کی روٹی + سلاد",
        "slot": "lunch",
        "tags": ["desi", "veg", "high_fiber", "low_sodium", "low_satfat", "light"],
        "carb_servings": 2,
        "notes": "Low GI daal. Protein rich. Avoid heavy tarka."
    },
    {
        "name":    "Palak (spinach) with paneer or chicken + 1 roti",
        "name_ur": "پالک پنیر یا چکن + 1 روٹی",
        "slot": "lunch",
        "tags": ["desi", "low_satfat", "high_fiber"],
        "carb_servings": 2,
        "notes": "Spinach adds iron and fibre. Light on cream or butter."
    },

    # ── AFTERNOON SNACK (snack_pm) ─────────────────────────────────────────────
    {
        "name":    "1 medium guava",
        "name_ur": "1 درمیانہ امرود",
        "slot": "snack_pm",
        "tags": ["veg", "high_fiber", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "Best fruit for diabetics — high fibre, low glycemic."
    },
    {
        "name":    "Small handful of roasted chana",
        "name_ur": "بھنے ہوئے چنے کی مٹھی",
        "slot": "snack_pm",
        "tags": ["desi", "veg", "high_fiber", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "High protein and fibre. Roasted, not fried."
    },
    {
        "name":    "Unsweetened yogurt with cucumber and mint",
        "name_ur": "بغیر چینی دہی کھیرے اور پودینے کے ساتھ",
        "slot": "snack_pm",
        "tags": ["desi", "veg", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "Cooling, filling and blood-sugar friendly."
    },
    {
        "name":    "1 small apple + 5 almonds",
        "name_ur": "1 چھوٹا سیب + 5 بادام",
        "slot": "snack_pm",
        "tags": ["veg", "high_fiber", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "Apple fibre slows sugar absorption. Almonds add healthy fat."
    },
    {
        "name":    "Roasted pumpkin seeds (1 small handful)",
        "name_ur": "بھنے ہوئے کدو کے بیج (1 چھوٹی مٹھی)",
        "slot": "snack_pm",
        "tags": ["desi", "veg", "low_sodium", "light"],
        "carb_servings": 0,
        "notes": "High in magnesium which helps insulin sensitivity."
    },
    {
        "name":    "Salted lassi (low-fat, no sugar)",
        "name_ur": "نمکین لسی (کم چکنائی، بغیر چینی)",
        "slot": "snack_pm",
        "tags": ["desi", "veg", "low_sodium"],
        "carb_servings": 1,
        "notes": "Salted lassi only — no sugar. Cooling and filling."
    },

    # ── DINNER ────────────────────────────────────────────────────────────────
    {
        "name":    "Baked or grilled fish + raita + green salad",
        "name_ur": "بیکڈ یا گرلڈ مچھلی + رائتہ + سبز سلاد",
        "slot": "dinner",
        "tags": ["desi", "low_satfat", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "Omega-3 + protein. Heart and blood-sugar friendly."
    },
    {
        "name":    "Daal tadka + 1 atta roti + cucumber slices",
        "name_ur": "دال تڑکہ + 1 آٹے کی روٹی + کھیرے کی سلائسیں",
        "slot": "dinner",
        "tags": ["desi", "veg", "high_fiber", "low_sodium"],
        "carb_servings": 2,
        "notes": "Low GI daal. Protein rich. Avoid heavy tarka."
    },
    {
        "name":    "Chicken karahi (less oil) + 1 atta roti + salad",
        "name_ur": "چکن کڑاہی (کم تیل) + 1 آٹے کی روٹی + سلاد",
        "slot": "dinner",
        "tags": ["desi", "low_satfat"],
        "carb_servings": 2,
        "notes": "Ask for less oil. Atta roti instead of naan."
    },
    {
        "name":    "Palak chicken + 1 roti + raita",
        "name_ur": "پالک چکن + 1 روٹی + رائتہ",
        "slot": "dinner",
        "tags": ["desi", "low_satfat", "high_fiber"],
        "carb_servings": 2,
        "notes": "Light on cream or butter. Spinach adds fibre."
    },
    {
        "name":    "Vegetable pulao (small portion) + plain yogurt + salad",
        "name_ur": "سبزی پلاؤ (چھوٹی مقدار) + سادہ دہی + سلاد",
        "slot": "dinner",
        "tags": ["desi", "veg", "low_satfat"],
        "carb_servings": 3,
        "notes": "Rice is high GI — keep to half katori. Add raita."
    },
    {
        "name":    "Masoor daal + 1 roti + tomato-onion salad",
        "name_ur": "مسور دال + 1 روٹی + ٹماٹر پیاز کا سلاد",
        "slot": "dinner",
        "tags": ["desi", "veg", "high_fiber", "low_sodium", "light"],
        "carb_servings": 2,
        "notes": "Very low GI. High fibre. Anti-inflammatory."
    },
    {
        "name":    "Karela (bitter melon) with chicken + 1 roti",
        "name_ur": "کریلا چکن + 1 روٹی",
        "slot": "dinner",
        "tags": ["desi", "low_satfat", "high_fiber"],
        "carb_servings": 2,
        "notes": "Bitter melon lowers blood sugar naturally."
    },
    {
        "name":    "Bhindi (okra) masala + 1 atta roti + plain yogurt",
        "name_ur": "بھنڈی مصالحہ + 1 آٹے کی روٹی + سادہ دہی",
        "slot": "dinner",
        "tags": ["desi", "veg", "high_fiber", "low_satfat", "low_sodium"],
        "carb_servings": 2,
        "notes": "Okra has blood sugar lowering properties."
    },

    # ── BEDTIME SNACK (snack_bed) ──────────────────────────────────────────────
    # Small, slow-release — prevents overnight hypo for insulin users.
    # Minimum 4 desi-tagged options to avoid same snack every night.
    {
        "name":    "1 small glass warm low-fat milk (unsweetened)",
        "name_ur": "1 چھوٹا گلاس گرم کم چکنائی والا دودھ (بغیر چینی)",
        "slot": "snack_bed",
        "tags": ["desi", "veg", "low_sodium"],
        "carb_servings": 1,
        "notes": "Slow-release protein. Helps prevent overnight blood sugar drops."
    },
    {
        "name":    "2 whole wheat crackers + 1 tsp peanut butter",
        "name_ur": "2 گندم کے کریکرز + 1 چائے کا چمچ مونگ پھلی کا مکھن",
        "slot": "snack_bed",
        "tags": ["veg", "low_sodium"],
        "carb_servings": 1,
        "notes": "Carb + protein combination keeps blood sugar stable overnight."
    },
    {
        "name":    "Small bowl of unsweetened yogurt + 5 almonds",
        "name_ur": "بغیر چینی دہی کا چھوٹا پیالہ + 5 بادام",
        "slot": "snack_bed",
        "tags": ["desi", "veg", "low_sodium"],
        "carb_servings": 1,
        "notes": "Protein slows overnight glucose drop. Good for insulin users."
    },
    {
        "name":    "Half a small apple + a few walnuts",
        "name_ur": "آدھا چھوٹا سیب + کچھ اخروٹ",
        "slot": "snack_bed",
        "tags": ["veg", "high_fiber", "low_sodium"],
        "carb_servings": 1,
        "notes": "Light and satisfying. Walnuts add omega-3 and slow sugar release."
    },
    {
        "name":    "Warm doodh (low-fat milk) with pinch of haldi (turmeric)",
        "name_ur": "گرم دودھ ہلدی کی چٹکی کے ساتھ",
        "slot": "snack_bed",
        "tags": ["desi", "veg", "low_sodium", "low_satfat"],
        "carb_servings": 1,
        "notes": "Haldi doodh — anti-inflammatory, slow protein release. No sugar."
    },
    {
        "name":    "1 small katori unsweetened dahi + 1 tsp flaxseeds",
        "name_ur": "1 چھوٹی کٹوری بغیر چینی دہی + 1 چائے کا چمچ السی",
        "slot": "snack_bed",
        "tags": ["desi", "veg", "low_sodium", "light"],
        "carb_servings": 1,
        "notes": "Probiotic + omega-3. Keeps blood sugar stable overnight."
    },
]

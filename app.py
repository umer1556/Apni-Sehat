import streamlit as st
import anthropic
import json
import random

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Apni Sehat | اپنی صحت",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  TRANSLATIONS
# ─────────────────────────────────────────────
T = {
    "en": {
        "app_title": "🩺 Apni Sehat",
        "app_subtitle": "Your personal health companion",
        "greeting": "Hi",
        "caution": "Caution — see doctor",
        "change_user": "🧑 Change User",
        "disclaimer_title": "⚠️ Medical Disclaimer",
        "disclaimer_body": "For information only — not medical advice.\n• Does not diagnose or prescribe\n• Does not replace your doctor\n• Always consult a qualified physician",
        "tab_meal": "🥗 Meal Plan",
        "tab_chat": "💬 Health Assistant",
        "tab_tips": "💡 Tips",
        "tab_progress": "📈 Progress",
        "select_day": "Select Day",
        "day_menu": "Menu —",
        "carbs": "carbs",
        "why_meal": "💡 Why this meal?",
        "new_plan": "🔄 New Plan",
        "desi_toggle": "🍛 Desi Preferred",
        "veg_toggle": "🥦 Vegetarian Only",
        "breakfast": "BREAKFAST",
        "lunch": "LUNCH",
        "snack": "AFTERNOON SNACK",
        "dinner": "DINNER",
        "chat_title": "💬 Ask Your Health Assistant",
        "chat_subtitle": "Ask anything about your diet or blood sugar — in English or Urdu.",
        "chat_placeholder": "Type your question here... (English or اردو)",
        "chat_bot_name": "SEHAT SAATHI",
        "chat_thinking": "Thinking...",
        "tip_today": "💡 Today's Health Tip",
        "days": ["Mon Day 1", "Tue Day 2", "Wed Day 3", "Thu Day 4", "Fri Day 5", "Sat Day 6", "Sun Day 7"],
        "eating_plan": "Eating Pattern: 3 Meals + 1 Snack",
        "eating_desc": "Standard pattern for stable blood sugar management.",
        "your_7day": "🥗 Your 7-Day Meal Plan",
    },
    "ur": {
        "app_title": "🩺 اپنی صحت",
        "app_subtitle": "آپ کا ذاتی صحت کا ساتھی",
        "greeting": "السلام علیکم",
        "caution": "احتیاط — ڈاکٹر سے ملیں 🟡",
        "change_user": "🧑 دوسرا شخص",
        "disclaimer_title": "⚠️ طبی وضاحت",
        "disclaimer_body": "صرف معلومات — طبی مشورہ نہیں۔\n• تشخیص یا دوائی تجویز نہیں کرتی\n• ڈاکٹر کی جگہ نہیں لیتی\n• ہمیشہ معالج سے رجوع کریں",
        "tab_meal": "🥗 کھانے کا منصوبہ",
        "tab_chat": "💬 صحت مددگار",
        "tab_tips": "💡 مشورے",
        "tab_progress": "📈 پیشرفت",
        "select_day": "دن منتخب کریں",
        "day_menu": "مینو —",
        "carbs": "کاربس",
        "why_meal": "💡 یہ کھانا کیوں؟",
        "new_plan": "🔄 نیا منصوبہ",
        "desi_toggle": "🍛 دیسی کھانا پسند ہے",
        "veg_toggle": "🥦 صرف سبزی خور",
        "breakfast": "ناشتہ",
        "lunch": "دوپہر کا کھانا",
        "snack": "شام کا ناشتہ",
        "dinner": "رات کا کھانا",
        "chat_title": "💬 اپنے صحت کے مددگار سے پوچھیں",
        "chat_subtitle": "خوراک یا بلڈ شوگر کے بارے میں کچھ بھی پوچھیں — اردو یا انگریزی میں۔",
        "chat_placeholder": "یہاں اپنا سوال لکھیں... (English یا اردو)",
        "chat_bot_name": "سیہت ساتھی",
        "chat_thinking": "سوچ رہا ہوں...",
        "tip_today": "💡 آج کا صحت مشورہ",
        "days": ["پیر دن ۱", "منگل دن ۲", "بدھ دن ۳", "جمعرات دن ۴", "جمعہ دن ۵", "ہفتہ دن ۶", "اتوار دن ۷"],
        "eating_plan": "کھانے کا ڈھانچہ: ۳ کھانے + ۱ ناشتہ",
        "eating_desc": "مستحکم بلڈ شوگر کے لیے معیاری منصوبہ۔",
        "your_7day": "🥗 آپ کا ۷ دن کا منصوبہ",
    },
}

# ─────────────────────────────────────────────
#  PAKISTANI DIABETES-FRIENDLY MEAL BANK
#  All meals with bilingual names & descriptions
# ─────────────────────────────────────────────
BREAKFASTS = [
    {
        "name": "Moong daal chilla + mint chutney",
        "name_ur": "مونگ دال چلّہ + پودینہ چٹنی",
        "carbs": 15,
        "desc": "High protein and fibre. Very gentle on blood sugar.",
        "desc_ur": "پروٹین اور فائبر سے بھرپور۔ بلڈ شوگر پر بہت ہلکا اثر۔",
        "tip": "Use a non-stick pan with minimal oil. Add chopped onion, green chilli and ajwain to batter.",
        "tip_ur": "نان اسٹک پین میں کم تیل استعمال کریں۔ آٹے میں پیاز، ہری مرچ اور اجوائن ملائیں۔",
        "veg": True,
    },
    {
        "name": "2 poached/boiled eggs + 1 slice atta bread",
        "name_ur": "۲ ابلے انڈے + ۱ آٹے کی روٹی",
        "carbs": 20,
        "desc": "Excellent protein start. Egg yolk is fine in moderation.",
        "desc_ur": "بہترین پروٹین ناشتہ۔ انڈے کی زردی اعتدال میں ٹھیک ہے۔",
        "tip": "Boil eggs for 8–10 minutes. Pair with a small tomato salad.",
        "tip_ur": "انڈے ۸–۱۰ منٹ ابالیں۔ چھوٹے ٹماٹر سلاد کے ساتھ کھائیں۔",
        "veg": False,
    },
    {
        "name": "Besan cheela + green chutney",
        "name_ur": "بیسن چلّہ + ہری چٹنی",
        "carbs": 18,
        "desc": "Chickpea flour is low GI and filling.",
        "desc_ur": "بیسن کا گلائیسیمک انڈیکس کم ہے اور پیٹ بھرتا ہے۔",
        "tip": "Add spinach and methi leaves to batter for extra fibre.",
        "tip_ur": "آٹے میں پالک اور میتھی ملائیں تاکہ فائبر بڑھے۔",
        "veg": True,
    },
    {
        "name": "Plain dahi (full fat) + 1 atta roti + cucumber",
        "name_ur": "سادہ دہی + ۱ آٹے کی روٹی + کھیرا",
        "carbs": 25,
        "desc": "Probiotics from dahi slow glucose absorption.",
        "desc_ur": "دہی کے پروبائیوٹکس گلوکوز جذب کو سست کرتے ہیں۔",
        "tip": "Use unsweetened full-fat dahi. Avoid flavoured yogurt.",
        "tip_ur": "بغیر چینی کا دہی استعمال کریں۔ فلیورڈ یوگرٹ سے پرہیز کریں۔",
        "veg": True,
    },
    {
        "name": "Oatmeal (no sugar) + pinch of cardamom + chopped almonds",
        "name_ur": "دلیہ (بغیر چینی) + الائچی + کٹے ہوئے بادام",
        "carbs": 28,
        "desc": "Beta-glucan fibre in oats reduces post-meal glucose spike.",
        "desc_ur": "جو کا بیٹا گلوکان ذیابیطس کے لیے بہترین ہے۔",
        "tip": "Sweeten with 2 drops of stevia if needed. Add a few walnuts for omega-3.",
        "tip_ur": "میٹھا کرنے کے لیے اسٹیویا استعمال کریں۔ اخروٹ بھی ڈال سکتے ہیں۔",
        "veg": True,
    },
    {
        "name": "Anda paratha (1, made with atta + little ghee) + raita",
        "name_ur": "انڈہ پراٹھا (۱، آٹے کا، تھوڑا گھی) + رائتہ",
        "carbs": 30,
        "desc": "Whole wheat keeps fibre high; egg adds protein.",
        "desc_ur": "گندم کا آٹا فائبر برقرار رکھتا ہے؛ انڈہ پروٹین دیتا ہے۔",
        "tip": "Use only 1 tsp ghee. Pair with cucumber-mint raita instead of pickle.",
        "tip_ur": "صرف ایک چائے کا چمچ گھی استعمال کریں۔ اچار کی جگہ رائتہ کھائیں۔",
        "veg": False,
    },
    {
        "name": "Methi (fenugreek) paratha × 1 + plain dahi",
        "name_ur": "میتھی پراٹھا × ۱ + سادہ دہی",
        "carbs": 22,
        "desc": "Fenugreek is proven to lower fasting blood sugar.",
        "desc_ur": "میتھی فاسٹنگ شوگر کم کرنے میں ثابت شدہ ہے۔",
        "tip": "Soak methi overnight to reduce bitterness. Use atta dough.",
        "tip_ur": "کڑواہٹ کم کرنے کے لیے میتھی رات بھر بھگوئیں۔ آٹے کا استعمال کریں۔",
        "veg": True,
    },
]

LUNCHES = [
    {
        "name": "Chana curry + 1 atta roti + kachumber salad",
        "name_ur": "چنے کی کری + ۱ آٹے کی روٹی + کچمبر سلاد",
        "carbs": 45,
        "desc": "Chickpeas are excellent for blood sugar. Avoid too much oil.",
        "desc_ur": "چنے بلڈ شوگر کے لیے بہترین ہیں۔ زیادہ تیل سے پرہیز کریں۔",
        "tip": "Cook chana with tomatoes, onion, cumin, and minimal oil. Skip tarka in dalda.",
        "tip_ur": "ٹماٹر، پیاز، زیرہ سے پکائیں، ڈالڈا تیل نہ ڈالیں۔",
        "veg": True,
    },
    {
        "name": "Daal mash + 1 atta roti + raw onion + green chilli",
        "name_ur": "دال ماش + ۱ آٹے کی روٹی + کچی پیاز + ہری مرچ",
        "carbs": 40,
        "desc": "White lentils are rich in protein and slow-digesting carbs.",
        "desc_ur": "ماش کی دال پروٹین اور آہستہ ہضم کاربس سے بھرپور ہے۔",
        "tip": "Add a squeeze of lemon juice. Limit oil in tarka to 1 tsp.",
        "tip_ur": "لیموں نچوڑیں۔ تڑکے میں صرف ایک چائے کا چمچ تیل ڈالیں۔",
        "veg": True,
    },
    {
        "name": "Chicken karahi (less oil) + 1 atta roti + salad",
        "name_ur": "مرغی کڑاہی (کم تیل) + ۱ آٹے کی روٹی + سلاد",
        "carbs": 30,
        "desc": "Ask for less oil. Atta roti instead of naan.",
        "desc_ur": "کم تیل میں بنائیں۔ نان کی جگہ آٹے کی روٹی کھائیں۔",
        "tip": "Use 1 tbsp oil max. Cook with tomatoes, ginger-garlic paste and spices.",
        "tip_ur": "زیادہ سے زیادہ ۱ کھانے کا چمچ تیل۔ ٹماٹر اور ادرک لہسن کے ساتھ پکائیں۔",
        "veg": False,
    },
    {
        "name": "Saag (spinach/mustard) + 1 makki ki roti",
        "name_ur": "ساگ (پالک/سرسوں) + ۱ مکئی کی روٹی",
        "carbs": 35,
        "desc": "Winter staple — iron-rich leafy greens with low GI corn roti.",
        "desc_ur": "سردیوں کا بہترین کھانا — آئرن سے بھرپور، کم GI مکئی کی روٹی۔",
        "tip": "Avoid adding too much butter or ghee. A small knob (1 tsp) is fine.",
        "tip_ur": "زیادہ مکھن یا گھی نہ ڈالیں۔ ایک چائے کا چمچ کافی ہے۔",
        "veg": True,
    },
    {
        "name": "Tarka daal (chana + moong mix) + 1 roti + cucumber raita",
        "name_ur": "ترکہ دال (چنہ + مونگ مکس) + ۱ روٹی + کھیرے کا رائتہ",
        "carbs": 42,
        "desc": "Mixed lentils provide complete amino acids and stable glucose.",
        "desc_ur": "مخلوط دالیں مکمل امینو ایسڈ اور مستحکم گلوکوز دیتی ہیں۔",
        "tip": "Use mustard oil for tarka — better fat profile than vegetable oil.",
        "tip_ur": "تڑکے کے لیے سرسوں کا تیل بہتر ہے۔",
        "veg": True,
    },
    {
        "name": "Karela (bitter gourd) bhujia + daal + 1 roti",
        "name_ur": "کریلا بھجیا + دال + ۱ روٹی",
        "carbs": 32,
        "desc": "Karela contains momordicin — a natural blood sugar reducer.",
        "desc_ur": "کریلے میں ممورڈیسین ہوتا ہے — قدرتی بلڈ شوگر کم کرنے والا۔",
        "tip": "Salt and squeeze karela before cooking to reduce bitterness. Cook with onions.",
        "tip_ur": "کریلے پر نمک لگا کر نچوڑیں پھر پکائیں، کڑواہٹ کم ہوگی۔",
        "veg": True,
    },
    {
        "name": "Grilled fish (rohu/tilapia) + aloo gobhi sabzi + 1 roti",
        "name_ur": "گرلڈ مچھلی (روہو/تلاپیا) + آلو گوبھی سبزی + ۱ روٹی",
        "carbs": 38,
        "desc": "Omega-3 from fish reduces inflammation linked to diabetes.",
        "desc_ur": "مچھلی کا اومیگا-3 ذیابیطس سے جڑی سوزش کم کرتا ہے۔",
        "tip": "Grill or shallow fry with minimal oil. Season with haldi, zeera, lemon.",
        "tip_ur": "کم تیل میں گرل یا ہلکا فرائی کریں۔ ہلدی، زیرہ، لیموں سے ذائقہ دیں۔",
        "veg": False,
    },
]

SNACKS = [
    {
        "name": "Plain dahi (1 cup) with sliced cucumber and mint",
        "name_ur": "سادہ دہی (۱ پیالی) کھیرے اور پودینے کے ساتھ",
        "carbs": 12,
        "desc": "Cooling, filling and blood-sugar friendly.",
        "desc_ur": "ٹھنڈک دیتا ہے، پیٹ بھرتا ہے، بلڈ شوگر دوست ہے۔",
        "tip": "Add a pinch of roasted zeera and kala namak for flavour.",
        "tip_ur": "ذائقے کے لیے بھنا زیرہ اور کالا نمک ڈالیں۔",
        "veg": True,
    },
    {
        "name": "Handful of mixed nuts (almonds + walnuts + peanuts)",
        "name_ur": "مٹھی بھر مخلوط مغزیات (بادام + اخروٹ + مونگ پھلی)",
        "carbs": 6,
        "desc": "Healthy fats slow glucose spikes. Keep to a small handful.",
        "desc_ur": "صحت مند چکنائی گلوکوز اضافہ روکتی ہے۔ چھوٹی مٹھی کافی ہے۔",
        "tip": "Avoid salted or roasted-in-oil varieties. Raw or dry roasted only.",
        "tip_ur": "نمکین یا تیل میں بھنے مغزیات سے پرہیز کریں۔ خشک بھنے استعمال کریں۔",
        "veg": True,
    },
    {
        "name": "Boiled chana chaat (no tamarind chutney)",
        "name_ur": "ابلے چنے کی چاٹ (بغیر اِملی چٹنی)",
        "carbs": 18,
        "desc": "Fibre-packed snack that keeps hunger away for hours.",
        "desc_ur": "فائبر سے بھرپور ناشتہ جو گھنٹوں بھوک نہیں لگنے دیتا۔",
        "tip": "Season with lemon, zeera, green chilli and fresh coriander. Skip the sweet chutney.",
        "tip_ur": "لیموں، زیرہ، ہری مرچ اور تازہ دھنیا ڈالیں۔ میٹھی چٹنی نہ ڈالیں۔",
        "veg": True,
    },
    {
        "name": "Apple (1 small, ~100g) with 10 almonds",
        "name_ur": "سیب (۱ چھوٹا، ~۱۰۰گرام) اور ۱۰ بادام",
        "carbs": 16,
        "desc": "Fruit fibre + nut fat = slower sugar release.",
        "desc_ur": "پھل کا فائبر + مغز کی چکنائی = آہستہ شوگر اخراج۔",
        "tip": "Eat apple with skin for maximum fibre. Avoid apple juice.",
        "tip_ur": "سیب چھلکے سمیت کھائیں تاکہ فائبر زیادہ ملے۔ جوس سے پرہیز کریں۔",
        "veg": True,
    },
    {
        "name": "Roasted makhana (fox nuts) — 1 cup",
        "name_ur": "بھنے ہوئے مخانے — ۱ پیالی",
        "carbs": 14,
        "desc": "Low GI, light and satisfying Pakistani-favourite snack.",
        "desc_ur": "کم GI، ہلکا اور پیٹ بھرنے والا پاکستانی پسندیدہ ناشتہ۔",
        "tip": "Dry roast with a pinch of black salt and zeera. No butter needed.",
        "tip_ur": "کالے نمک اور زیرے کے ساتھ خشک بھونیں۔ مکھن کی ضرورت نہیں۔",
        "veg": True,
    },
]

DINNERS = [
    {
        "name": "Palak gosht (spinach mutton — small portion) + 1 atta roti",
        "name_ur": "پالک گوشت (چھوٹا حصہ) + ۱ آٹے کی روٹی",
        "carbs": 28,
        "desc": "Iron-rich spinach with lean mutton. Portion control is key.",
        "desc_ur": "آئرن سے بھرپور پالک اور دبلے گوشت کا مجموعہ۔ مقدار کا خیال رکھیں۔",
        "tip": "Use lean cuts. Trim fat. Limit to 60–80g meat. Ask for less oil.",
        "tip_ur": "دبلے گوشت کا استعمال کریں۔ ۶۰–۸۰ گرام تک محدود رکھیں۔",
        "veg": False,
    },
    {
        "name": "Aloo palak (small potato, lots of spinach) + 1 roti",
        "name_ur": "آلو پالک (کم آلو، زیادہ پالک) + ۱ روٹی",
        "carbs": 33,
        "desc": "Keep potato portion small — spinach is the star here.",
        "desc_ur": "آلو کم رکھیں — اصل فائدہ پالک سے ہے۔",
        "tip": "Use only 1 small potato per serving. Load up on spinach instead.",
        "tip_ur": "ایک چھوٹا آلو کافی ہے۔ پالک زیادہ ڈالیں۔",
        "veg": True,
    },
    {
        "name": "Daal lentil soup + 1 roti + raw salad",
        "name_ur": "دال کا سوپ + ۱ روٹی + کچا سلاد",
        "carbs": 38,
        "desc": "Light dinner — ideal for diabetes management at night.",
        "desc_ur": "ہلکا رات کا کھانا — ذیابیطس میں رات کے لیے بہترین۔",
        "tip": "Keep dinner light. Avoid eating after 8pm. Walk 10 minutes after eating.",
        "tip_ur": "رات کا کھانا ہلکا رکھیں۔ رات ۸ بجے کے بعد نہ کھائیں۔ ۱۰ منٹ چہل قدمی کریں۔",
        "veg": True,
    },
    {
        "name": "Chicken shorba (broth) + 1 atta roti",
        "name_ur": "مرغی کا شوربہ + ۱ آٹے کی روٹی",
        "carbs": 25,
        "desc": "Light soup-based dinner — excellent for blood sugar at night.",
        "desc_ur": "ہلکا شوربہ والا کھانا — رات کی بلڈ شوگر کے لیے عمدہ۔",
        "tip": "Skip cream or coconut milk. Add sabz dhaniya and ginger for flavour.",
        "tip_ur": "کریم یا ناریل دودھ نہ ڈالیں۔ دھنیا اور ادرک ڈالیں۔",
        "veg": False,
    },
    {
        "name": "Mixed vegetable curry (gajar, tori, shimla mirch) + 1 roti",
        "name_ur": "مخلوط سبزی (گاجر، توری، شملہ مرچ) + ۱ روٹی",
        "carbs": 30,
        "desc": "Rainbow vegetables provide antioxidants that protect diabetics.",
        "desc_ur": "رنگین سبزیاں اینٹی آکسیڈنٹ فراہم کرتی ہیں جو ذیابیطسی کی حفاظت کرتے ہیں۔",
        "tip": "Cook in mustard oil with whole spices. Avoid store-bought masala mixes.",
        "tip_ur": "سرسوں کے تیل اور صابت مصالحوں میں پکائیں۔ پیکٹ مصالحے سے پرہیز کریں۔",
        "veg": True,
    },
    {
        "name": "Grilled seekh kebab (2 pieces) + mint chutney + salad",
        "name_ur": "گرلڈ سیخ کباب (۲ عدد) + پودینہ چٹنی + سلاد",
        "carbs": 8,
        "desc": "High protein, very low carb — excellent for blood sugar.",
        "desc_ur": "زیادہ پروٹین، بہت کم کاربس — بلڈ شوگر کے لیے بہترین۔",
        "tip": "Grill or bake. Avoid frying. Skip the naan — have salad instead.",
        "tip_ur": "گرل یا بیک کریں۔ فرائی نہ کریں۔ نان چھوڑیں، سلاد کھائیں۔",
        "veg": False,
    },
    {
        "name": "Masoor daal + 1 roti + boiled egg",
        "name_ur": "مسور دال + ۱ روٹی + ابلا انڈہ",
        "carbs": 36,
        "desc": "Red lentils digest slowly and are packed with folate.",
        "desc_ur": "مسور دال آہستہ ہضم ہوتی ہے اور فولیٹ سے بھرپور ہے۔",
        "tip": "Cook without too much ghee. A single tsp for tarka is sufficient.",
        "tip_ur": "زیادہ گھی نہ ڈالیں۔ تڑکے کے لیے ایک چائے کا چمچ کافی ہے۔",
        "veg": False,
    },
]

TIPS = {
    "en": [
        "🚶 Walk 20–30 minutes after lunch. Even a slow walk cuts post-meal glucose by up to 30%.",
        "💧 Drink 8–10 glasses of water daily. Dehydration raises blood sugar.",
        "🧂 Reduce salt — hypertension and diabetes together damage kidneys faster.",
        "😴 Sleep 7–8 hours. Poor sleep raises cortisol which spikes blood sugar.",
        "🍽️ Eat slowly and chew well. It takes 20 minutes for your brain to register fullness.",
        "📉 Check blood sugar 2 hours after meals to see how each food affects you.",
        "🥗 Fill half your plate with sabziyat (vegetables) at every meal.",
        "🚫 Avoid shakar, gur, honey and fruit juices — all spike blood sugar fast.",
        "🏃 Even 10 minutes of light exercise after dinner helps overnight glucose levels.",
        "📅 Keep a small food diary — it's the most powerful diabetes tool there is.",
    ],
    "ur": [
        "🚶 دوپہر کے کھانے کے بعد ۲۰–۳۰ منٹ چہل قدمی کریں۔ یہ کھانے کے بعد بلڈ شوگر ۳۰٪ تک کم کر سکتی ہے۔",
        "💧 روزانہ ۸–۱۰ گلاس پانی پیئں۔ پانی کی کمی بلڈ شوگر بڑھاتی ہے۔",
        "🧂 نمک کم کریں — ہائی بلڈ پریشر اور ذیابیطس مل کر گردوں کو جلد نقصان پہنچاتے ہیں۔",
        "😴 ۷–۸ گھنٹے سوئیں۔ نیند کی کمی کورٹیسول بڑھاتی ہے جو بلڈ شوگر اوپر کر دیتی ہے۔",
        "🍽️ آہستہ کھائیں اور اچھی طرح چبائیں۔ دماغ کو پیٹ بھرنے کا احساس ۲۰ منٹ بعد ہوتا ہے۔",
        "📉 کھانے کے ۲ گھنٹے بعد بلڈ شوگر چیک کریں تاکہ معلوم ہو کہ کون سا کھانا کیسا اثر ڈالتا ہے۔",
        "🥗 ہر کھانے میں آدھی پلیٹ سبزیاں رکھیں۔",
        "🚫 شکر، گڑ، شہد اور پھلوں کے جوس سے پرہیز کریں — یہ سب بلڈ شوگر تیزی سے بڑھاتے ہیں۔",
        "🏃 رات کے کھانے کے بعد ۱۰ منٹ کی ہلکی ورزش رات بھر کی بلڈ شوگر بہتر کرتی ہے۔",
        "📅 ایک چھوٹی کھانے کی ڈائری رکھیں — یہ ذیابیطس کا سب سے طاقتور ہتھیار ہے۔",
    ],
}

# ─────────────────────────────────────────────
#  GENERATE 7-DAY MEAL PLAN
# ─────────────────────────────────────────────
def generate_meal_plan(vegetarian=False):
    plan = []
    b_pool = [m for m in BREAKFASTS if not vegetarian or m["veg"]]
    l_pool = [m for m in LUNCHES if not vegetarian or m["veg"]]
    s_pool = [m for m in SNACKS if not vegetarian or m["veg"]]
    d_pool = [m for m in DINNERS if not vegetarian or m["veg"]]

    # Ensure we have enough unique meals
    b_pool = (b_pool * 3)[:7]
    l_pool = (l_pool * 3)[:7]
    s_pool = (s_pool * 3)[:7]
    d_pool = (d_pool * 3)[:7]

    random.shuffle(b_pool)
    random.shuffle(l_pool)
    random.shuffle(s_pool)
    random.shuffle(d_pool)

    for i in range(7):
        plan.append({
            "breakfast": b_pool[i % len(b_pool)],
            "lunch": l_pool[i % len(l_pool)],
            "snack": s_pool[i % len(s_pool)],
            "dinner": d_pool[i % len(d_pool)],
        })
    return plan

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "ur"
if "user_name" not in st.session_state:
    st.session_state.user_name = "umer"
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = generate_meal_plan()
if "vegetarian" not in st.session_state:
    st.session_state.vegetarian = False
if "desi_preferred" not in st.session_state:
    st.session_state.desi_preferred = True
if "selected_day" not in st.session_state:
    st.session_state.selected_day = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "condition" not in st.session_state:
    st.session_state.condition = "Type 2 Diabetes"

lang = st.session_state.lang
t = T[lang]

# ─────────────────────────────────────────────
#  CUSTOM CSS  (dark theme)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu&family=Inter:wght@400;600;700&display=swap');

:root {
    --bg: #0e1117;
    --card: #1a1d24;
    --card2: #22262f;
    --green: #22c55e;
    --green-dark: #16a34a;
    --yellow: #eab308;
    --red: #ef4444;
    --text: #f1f5f9;
    --muted: #94a3b8;
    --border: #2d3748;
    --accent: #3b82f6;
}

html, body, [data-testid="stApp"] { background: var(--bg) !important; color: var(--text) !important; }

.stButton > button {
    background: var(--card2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: var(--green-dark) !important;
    border-color: var(--green) !important;
    color: white !important;
}

.meal-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.6rem;
    border-left: 4px solid var(--green);
}
.meal-type {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--green);
    margin-bottom: 0.3rem;
}
.meal-name {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 0.25rem;
}
.meal-name-ur {
    font-family: 'Noto Nastaliq Urdu', serif;
    font-size: 1.1rem;
    direction: rtl;
    text-align: right;
    color: var(--text);
}
.meal-meta {
    font-size: 0.85rem;
    color: var(--muted);
}
.chat-bubble-user {
    background: var(--green-dark);
    color: white;
    border-radius: 14px 14px 4px 14px;
    padding: 0.8rem 1.1rem;
    margin: 0.4rem 0;
    max-width: 80%;
    margin-left: auto;
    font-size: 0.95rem;
}
.chat-bubble-bot {
    background: var(--card2);
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 14px 14px 14px 4px;
    padding: 0.8rem 1.1rem;
    margin: 0.4rem 0;
    max-width: 85%;
    font-size: 0.95rem;
    line-height: 1.6;
}
.chat-bubble-ur {
    font-family: 'Noto Nastaliq Urdu', serif;
    direction: rtl;
    text-align: right;
    font-size: 1.05rem;
    line-height: 2;
}
.chat-sender {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: var(--muted);
    margin-bottom: 0.2rem;
}
.disclaimer-box {
    background: #1c1a09;
    border: 1px solid #854d0e;
    border-radius: 10px;
    padding: 0.9rem;
    font-size: 0.8rem;
    color: #fde68a;
    white-space: pre-line;
}
.day-btn-active > button {
    background: var(--green-dark) !important;
    border-color: var(--green) !important;
    color: white !important;
}
.tip-box {
    background: #0f1f10;
    border: 1px solid var(--green-dark);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.95rem;
    color: #bbf7d0;
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    # Language toggle
    col_l, col_r = st.columns(2)
    with col_l:
        if st.button("🌐 English", use_container_width=True,
                     type="primary" if lang == "en" else "secondary"):
            st.session_state.lang = "en"
            st.rerun()
    with col_r:
        if st.button("🌐 اردو", use_container_width=True,
                     type="primary" if lang == "ur" else "secondary"):
            st.session_state.lang = "ur"
            st.rerun()

    st.markdown("---")
    st.markdown(f"### {t['app_title']}")
    st.caption(t["app_subtitle"])
    st.markdown("")

    greeting_text = f"**{t['greeting']}, {st.session_state.user_name}!**"
    st.success(greeting_text)
    st.warning(t["caution"])

    st.markdown("")
    if st.button(t["change_user"], use_container_width=True):
        st.session_state.chat_history = []
        new_name = "ali" if st.session_state.user_name == "umer" else "umer"
        st.session_state.user_name = new_name
        st.rerun()

    st.markdown("---")
    st.markdown(f"""<div class="disclaimer-box"><b>{t['disclaimer_title']}</b><br><br>{t['disclaimer_body']}</div>""",
                unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAIN TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([t["tab_meal"], t["tab_chat"], t["tab_tips"]])

# ──────────────────────────────────────────────────────────────────
#  TAB 1 — MEAL PLAN
# ──────────────────────────────────────────────────────────────────
with tab1:
    # Header
    col_h1, col_h2, col_h3 = st.columns([3, 1, 1])
    with col_h1:
        st.subheader(t["your_7day"])
    with col_h2:
        new_desi = st.toggle(t["desi_toggle"], value=st.session_state.desi_preferred)
        if new_desi != st.session_state.desi_preferred:
            st.session_state.desi_preferred = new_desi
    with col_h3:
        new_veg = st.toggle(t["veg_toggle"], value=st.session_state.vegetarian)
        if new_veg != st.session_state.vegetarian:
            st.session_state.vegetarian = new_veg
            st.session_state.meal_plan = generate_meal_plan(vegetarian=new_veg)
            st.rerun()

    # Eating pattern info
    st.info(f"**{t['eating_plan']}**  \n{t['eating_desc']}")

    # Today's tip
    tip_list = TIPS[lang]
    today_tip = tip_list[st.session_state.selected_day % len(tip_list)]
    st.markdown(f"<div class='tip-box'><b>{t['tip_today']}</b><br>{today_tip}</div>", unsafe_allow_html=True)
    st.markdown("")

    # New plan button
    col_np = st.columns([1, 3])
    with col_np[0]:
        if st.button(t["new_plan"]):
            st.session_state.meal_plan = generate_meal_plan(vegetarian=st.session_state.vegetarian)
            st.rerun()

    st.markdown(f"#### {t['select_day']}")

    # Day selector buttons
    day_cols = st.columns(7)
    for i, day_cols_item in enumerate(day_cols):
        with day_cols_item:
            if st.button(t["days"][i], key=f"day_{i}", use_container_width=True):
                st.session_state.selected_day = i
                st.rerun()

    st.markdown("---")
    day_idx = st.session_state.selected_day
    day_plan = st.session_state.meal_plan[day_idx]
    total_carbs = (day_plan["breakfast"]["carbs"] + day_plan["lunch"]["carbs"]
                   + day_plan["snack"]["carbs"] + day_plan["dinner"]["carbs"])

    day_label = t["days"][day_idx]
    st.markdown(f"### 📅 {t['day_menu']} {day_label} &nbsp; <span style='color:#94a3b8;font-size:0.9rem'>~{total_carbs}g {t['carbs']}</span>",
                unsafe_allow_html=True)
    st.markdown("")

    meal_types = [
        ("breakfast", "🟠", t["breakfast"]),
        ("lunch", "🟡", t["lunch"]),
        ("snack", "🟠", t["snack"]),
        ("dinner", "🌙", t["dinner"]),
    ]

    for meal_key, emoji, meal_label in meal_types:
        meal = day_plan[meal_key]
        name_display = meal["name_ur"] if lang == "ur" else meal["name"]
        desc_display = meal["desc_ur"] if lang == "ur" else meal["desc"]
        tip_display = meal["tip_ur"] if lang == "ur" else meal["tip"]

        name_class = "meal-name-ur" if lang == "ur" else "meal-name"
        dir_attr = 'dir="rtl"' if lang == "ur" else ""

        st.markdown(f"""
        <div class="meal-card">
            <div class="meal-type">{emoji} {meal_label}</div>
            <div class="{name_class}" {dir_attr}>{name_display}</div>
            <div class="meal-meta" {dir_attr}>~{meal['carbs']}g {t['carbs']} &nbsp;·&nbsp; {desc_display}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander(t["why_meal"]):
            st.markdown(f'<div {dir_attr}>{tip_display}</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────
#  TAB 2 — CHATBOT  (Sehat Saathi)
# ──────────────────────────────────────────────────────────────────
with tab2:
    st.subheader(t["chat_title"])
    st.caption(t["chat_subtitle"])
    st.markdown("---")

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display:flex;flex-direction:column;align-items:flex-end;margin-bottom:0.5rem">
                <div class="chat-sender">{st.session_state.user_name.upper()}</div>
                <div class="chat-bubble-user">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            ur_class = "chat-bubble-ur" if lang == "ur" else ""
            st.markdown(f"""
            <div style="display:flex;flex-direction:column;align-items:flex-start;margin-bottom:0.5rem">
                <div class="chat-sender">{t['chat_bot_name']}</div>
                <div class="chat-bubble-bot {ur_class}">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)

    # Input
    user_input = st.chat_input(t["chat_placeholder"])

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Build system prompt — enforce Urdu response when lang is ur
        language_instruction = (
            "IMPORTANT: The user interface is currently set to URDU. You MUST reply entirely in Urdu script "
            "(Nastaliq/Urdu). Do NOT use English in your response, except for food names that have no Urdu equivalent "
            "(e.g. 'GI index', 'HbA1c') — those you may keep in English within an otherwise Urdu response."
            if lang == "ur"
            else "Reply in clear, friendly English."
        )

        # Current meal plan context
        day = st.session_state.selected_day
        dp = st.session_state.meal_plan[day]
        meal_context = (
            f"Today's meal plan (Day {day+1}): "
            f"Breakfast: {dp['breakfast']['name']}, "
            f"Lunch: {dp['lunch']['name']}, "
            f"Snack: {dp['snack']['name']}, "
            f"Dinner: {dp['dinner']['name']}."
        )

        system_prompt = f"""You are Sehat Saathi (سیہت ساتھی), a warm, knowledgeable Pakistani health assistant 
specialising in Type 2 diabetes management for Pakistani patients. 

{language_instruction}

About this patient:
- Name: {st.session_state.user_name}
- Condition: {st.session_state.condition}
- {meal_context}

Your guidelines:
1. Give practical, culturally appropriate advice for Pakistani food culture (roti, daal, karahi, biryani, etc.)
2. Always remind users you are not a doctor and serious concerns need a physician
3. Be warm and encouraging — never judgmental about food choices
4. Keep responses concise (3–5 short paragraphs max)
5. Reference their actual meal plan when relevant
6. Use Pakistani food terminology naturally (roti, karahi, daal, sabzi, etc.)
7. {language_instruction}"""

        try:
            client = anthropic.Anthropic()
            messages_for_api = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.chat_history
            ]

            with st.spinner(t["chat_thinking"]):
                response = client.messages.create(
                    model="claude-opus-4-6",
                    max_tokens=600,
                    system=system_prompt,
                    messages=messages_for_api,
                )
            bot_reply = response.content[0].text
        except Exception as e:
            bot_reply = (
                f"معذرت، ابھی جواب دینے میں مسئلہ آیا۔ ({str(e)})"
                if lang == "ur"
                else f"Sorry, I couldn't connect right now. ({str(e)})"
            )

        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        st.rerun()

    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat" if lang == "en" else "🗑️ چیٹ صاف کریں"):
            st.session_state.chat_history = []
            st.rerun()

# ──────────────────────────────────────────────────────────────────
#  TAB 3 — TIPS
# ──────────────────────────────────────────────────────────────────
with tab3:
    st.subheader(t["tip_today"] + "s" if lang == "en" else "💡 صحت کے مشورے")
    dir_attr = 'dir="rtl" style="text-align:right;font-family:Noto Nastaliq Urdu,serif;font-size:1.05rem;line-height:2.2"' if lang == "ur" else ""
    for tip in TIPS[lang]:
        st.markdown(
            f'<div class="tip-box" {dir_attr} style="margin-bottom:0.8rem">{tip}</div>',
            unsafe_allow_html=True
        )

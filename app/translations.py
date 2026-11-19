"""
Translations dictionary and localization helpers for Schemate AI.
Supports English ('en'), Hindi ('hi'), and Hinglish ('hinglish').
"""

TRANSLATIONS = {
    "en": {
        # Navigation & Brand
        "app_title": "Schemate AI",
        "app_tagline": "AI Assistant for Indian Government Schemes",
        "nav_recommendations": "🎯 Scheme Recommendations",
        "nav_chat": "💬 AI Copilot (Chat)",
        "nav_profile": "👤 My Profile",
        "nav_language": "🌐 Language",
        "logout": "🚪 Log Out",
        
        # Language Selection Screen
        "choose_language_title": "Choose Your Preferred Language",
        "choose_language_subtitle": "Select your language for personalized scheme discovery and conversational assistance.",
        "lang_en_name": "English",
        "lang_en_desc": "Simple English with official government terminology",
        "lang_hi_name": "हिंदी (Hindi)",
        "lang_hi_desc": "सरल और स्पष्ट हिंदी में संपूर्ण जानकारी",
        "lang_hinglish_name": "Hinglish",
        "lang_hinglish_desc": "Everyday Hindi in English script (Aasan Hinglish)",
        
        # Onboarding Flow
        "onboarding_title": "Personalized Scheme Eligibility Onboarding",
        "onboarding_subtitle": "Answer a few questions so Schemate can match you with eligible central and state government schemes.",
        "step_1": "1. Language",
        "step_2": "2. Basic Details",
        "step_3": "3. Occupation & Income",
        "step_4": "4. Social Category & Specifics",
        "step_indicator": "Step {current} of {total}: {title}",
        
        # Form Fields - Basic
        "age_label": "Your Age (Years)",
        "age_help": "Schemes have specific minimum and maximum age criteria.",
        "dob_label": "Date of Birth (Optional)",
        "gender_label": "Gender",
        "gender_male": "Male",
        "gender_female": "Female",
        "gender_transgender": "Transgender",
        "gender_other": "Prefer not to say",
        "state_label": "State / Union Territory of Residence",
        "district_label": "District",
        "district_placeholder": "e.g., Bhopal, Indore, Jaipur, Patna",
        
        # Form Fields - Occupation & Income
        "occupation_label": "Primary Occupation",
        "occ_student": "Student",
        "occ_farmer": "Farmer / Agriculture",
        "occ_entrepreneur": "Entrepreneur / MSME / Business Owner",
        "occ_salaried": "Salaried Employee (Private / Govt)",
        "occ_self_employed": "Self-Employed / Freelancer / Professional",
        "occ_daily_wage": "Daily Wage Worker / Laborer / Artisan",
        "occ_unemployed": "Unemployed / Job Seeker",
        "occ_homemaker": "Homemaker",
        "occ_retired": "Senior Citizen / Retired",
        "occ_other": "Other",
        
        "income_label": "Annual Family Income (₹ in INR)",
        "income_help": "Combined gross annual income of your family.",
        "income_slab_label": "Quick Income Range",
        "income_below_1l": "Below ₹1,00,000 (BPL / Very Low Income)",
        "income_1l_2_5l": "₹1,00,000 - ₹2,50,000 (Low Income / EWS)",
        "income_2_5l_5l": "₹2,50,000 - ₹5,00,000 (Lower Middle)",
        "income_5l_8l": "₹5,00,000 - ₹8,00,000 (Middle / EWS Ceiling)",
        "income_above_8l": "Above ₹8,00,000",
        
        "education_label": "Highest Education Level",
        "edu_below_10th": "Below 10th Standard",
        "edu_10th": "10th Standard Pass (Matriculation)",
        "edu_12th": "12th Standard Pass (Intermediate)",
        "edu_diploma": "Diploma / Vocational / ITI",
        "edu_graduate": "Graduate / Bachelor's Degree",
        "edu_post_graduate": "Post Graduate / Master's Degree",
        "edu_doctorate": "Doctorate / Ph.D.",
        
        # Conditional - Student
        "student_section": "🎓 Student Details",
        "student_level_label": "Current Education Level",
        "student_level_ug": "Undergraduate (B.Tech, B.Sc, B.Com, MBBS)",
        "student_level_pg": "Postgraduate (M.Tech, M.Sc, MBA)",
        "student_level_school": "School (Class 9-12)",
        "student_level_phd": "Ph.D. / Research Fellowship",
        "student_level_diploma": "Diploma / ITI",
        "student_course_label": "Course / Field of Study",
        "student_course_placeholder": "e.g., B.Tech, B.Sc Agriculture, MBBS, B.Com, Class 12",
        "student_inst_label": "Institution Type",
        "inst_govt": "Government Institution",
        "inst_aided": "Government-Aided Institution",
        "inst_private": "Private Institution",
        
        # Conditional - Farmer
        "farmer_section": "🌾 Farmer & Agricultural Details",
        "farmer_ownership_label": "Land Ownership Status",
        "farmer_owner": "Owner Cultivator (Owns Agricultural Land)",
        "farmer_tenant": "Tenant Farmer / Sharecropper",
        "farmer_laborer": "Landless Agricultural Laborer",
        "farmer_land_label": "Landholding Size",
        "land_marginal": "Marginal (< 1 Hectare / < 2.5 Acres)",
        "land_small": "Small (1 to 2 Hectares / 2.5 - 5 Acres)",
        "land_medium_large": "Medium or Large (> 2 Hectares / > 5 Acres)",
        "land_none": "No Agricultural Land (Landless)",
        
        # Conditional - Entrepreneur
        "entrepreneur_section": "💼 Business & Enterprise Details",
        "business_type_label": "Business Sector",
        "biz_manufacturing": "Manufacturing / Industrial",
        "biz_services": "Services / IT / Consulting",
        "biz_trading": "Trading / Retail / Shopkeeper",
        "biz_agri_allied": "Agriculture Allied / Food Processing",
        "biz_handicraft": "Handloom / Handicrafts / Artisan Unit",
        "business_stage_label": "Business Stage",
        "biz_ideation": "Ideation / Planning (New Setup)",
        "biz_early": "Early Stage / Seed (< 2 Years Operating)",
        "biz_established": "Established / Expanding (> 2 Years)",
        
        # Social Category & Sensitive Information
        "social_category_label": "Social Category (Optional)",
        "cat_general": "General / Unreserved",
        "cat_obc": "OBC (Other Backward Class)",
        "cat_sc": "SC (Scheduled Caste)",
        "cat_st": "ST (Scheduled Tribe)",
        "cat_ews": "EWS (Economically Weaker Section)",
        "cat_minority": "Minority Community",
        
        "disability_label": "Disability Status (Optional)",
        "dis_none": "None",
        "dis_locomotor": "Locomotor / Physical Disability (≥ 40%)",
        "dis_visual": "Visual Impairment / Blindness / Low Vision",
        "dis_hearing": "Hearing Impairment / Speech",
        "dis_intellectual": "Intellectual / Multiple Disabilities",
        "dis_other": "Other Benchmark Disability",
        
        "marital_label": "Marital Status (Optional)",
        "mar_single": "Single / Unmarried",
        "mar_married": "Married",
        "mar_widowed": "Widowed",
        "mar_divorced": "Divorced / Separated",
        
        "sensitive_info_notice": "🔒 **Why we ask this:** Category, income, and disability details are used strictly to evaluate statutory welfare criteria, reserved quotas, and government subsidies. Your data is never shared.",
        
        # Buttons & Actions
        "btn_next": "Next Step →",
        "btn_back": "← Back",
        "btn_skip": "Skip Optional Questions",
        "btn_complete": "Save Profile & Discover Schemes 🎉",
        "btn_update": "Update Profile & Recalculate",
        "btn_cancel": "Cancel",
        "btn_refresh": "🔄 Recalculate Recommendations",
        "btn_edit_profile": "✏️ Edit Profile",
        "btn_ask_schemate": "💬 Ask Schemate About This",
        "btn_official_link": "🔗 Official Application Portal",
        "btn_view_details": "📄 View Scheme Details",
        "btn_go_to_chat": "💬 Continue to Schemate Copilot",
        
        # Recommendations Dashboard
        "rec_title": "Your Recommended Government Schemes",
        "rec_subtitle": "Personalized schemes evaluated deterministically against your verified profile attributes.",
        "filter_all": "All Schemes",
        "filter_eligible": "✅ Potentially Eligible",
        "filter_verification": "⚠️ Needs Verification",
        "filter_not_eligible": "❌ Not Eligible",
        "badge_eligible": "Potentially Eligible",
        "badge_verification": "Needs Verification",
        "badge_not_eligible": "Not Eligible",
        "tag_central": "🏛️ Central Scheme",
        "tag_state": "📍 State Scheme",
        "why_matches_title": "🎯 Why This Scheme Matches You",
        "missing_info_title": "⚠️ Missing Information / Needs Verification",
        "benefits_title": "🎁 Key Benefits",
        "documents_title": "📋 Required Documents",
        "official_sources_title": "🏛️ Official Sources & Department",
        "empty_recommendations": "No schemes found matching the selected filter.",
        "disclaimer_text": "⚠️ **Disclaimer:** Recommendations are based on published government criteria evaluated against your profile. Eligibility is not guaranteed and requires official verification by the concerned department upon application.",
        
        # Messages & Validation
        "val_age_required": "Please provide a valid age between 1 and 120.",
        "val_state_required": "Please select your state of residence.",
        "val_income_required": "Please enter your annual family income.",
        "profile_saved_success": "Profile saved successfully! Recalculating personalized recommendations...",

        # Saved Schemes
        "nav_saved_schemes": "⭐ My Saved Schemes",
        "saved_title": "My Saved Schemes",
        "saved_subtitle": "Keep track of government schemes that matter to you.",
        "saved_stat_total": "Total Saved Schemes",
        "saved_stat_eligible": "Potentially Eligible",
        "saved_stat_verify": "Needs Verification",
        "saved_search_placeholder": "Search saved schemes by name or keyword...",
        "saved_filter_all_types": "All Types",
        "saved_filter_central": "Central Schemes",
        "saved_filter_state": "State Schemes",
        "saved_filter_all_cats": "All Categories",
        "saved_sort_recent": "Recently Saved",
        "saved_sort_az": "Scheme Name (A-Z)",
        "saved_empty_title": "No saved schemes yet",
        "saved_empty_subtitle": "Explore government schemes and save the ones that interest you.",
        "saved_btn_explore": "🔍 Explore Schemes",
        "saved_btn_remove": "Remove from Saved",
        "saved_btn_saved": "✓ Saved",
        "saved_btn_save": "⭐ Save Scheme",
        "saved_notes_title": "📝 Personal Notes",
        "saved_notes_placeholder": "Add your private notes (e.g. Need to check income certificate, apply before next month)...",
        "saved_notes_save": "Save Notes",
        "saved_notes_saved_toast": "Notes updated successfully!",
        "saved_checklist_title": "📋 Required Documents Checklist",
        "saved_checklist_empty": "No specific document requirements listed.",
        "saved_toast_saved": "Scheme saved to your collection!",
        "saved_toast_removed": "Scheme removed from your saved list.",
    },
    
    "hi": {
        # Navigation & Brand
        "app_title": "Schemate AI",
        "app_tagline": "भारतीय सरकारी योजनाओं के लिए आपका AI सहायक",
        "nav_recommendations": "🎯 अनुशंसित योजनाएं",
        "nav_chat": "💬 AI चैटबॉट",
        "nav_profile": "👤 मेरी प्रोफ़ाइल",
        "nav_language": "🌐 भाषा",
        "logout": "🚪 लॉग आउट",
        
        # Language Selection Screen
        "choose_language_title": "अपनी पसंदीदा भाषा चुनें",
        "choose_language_subtitle": "व्यक्तिगत योजना खोज और सहायता के लिए अपनी पसंदीदा भाषा का चयन करें।",
        "lang_en_name": "English",
        "lang_en_desc": "सरल अंग्रेजी आधिकारिक सरकारी शब्दावली के साथ",
        "lang_hi_name": "हिंदी (Hindi)",
        "lang_hi_desc": "सरल और स्पष्ट हिंदी में संपूर्ण जानकारी",
        "lang_hinglish_name": "Hinglish",
        "lang_hinglish_desc": "रोमन लिपि में रोजमर्रा की हिंदी (Aasan Hinglish)",
        
        # Onboarding Flow
        "onboarding_title": "व्यक्तिगत योजना पात्रता ऑनबोर्डिंग",
        "onboarding_subtitle": "कुछ सवालों के जवाब दें ताकि Schemate आपको केंद्र और राज्य सरकार की योजनाओं से जोड़ सके।",
        "step_1": "1. भाषा",
        "step_2": "2. बुनियादी विवरण",
        "step_3": "3. व्यवसाय एवं आय",
        "step_4": "4. सामाजिक श्रेणी एवं विशेष विवरण",
        "step_indicator": "चरण {current}/{total}: {title}",
        
        # Form Fields - Basic
        "age_label": "आपकी आयु (वर्ष)",
        "age_help": "योजनाओं में विशिष्ट न्यूनतम और अधिकतम आयु मानदंड होते हैं।",
        "dob_label": "जन्म तिथि (वैकल्पिक)",
        "gender_label": "लिंग",
        "gender_male": "पुरुष",
        "gender_female": "महिला",
        "gender_transgender": "ट्रांसजेंडर",
        "gender_other": "बताना नहीं चाहते",
        "state_label": "निवास का राज्य / केंद्र शासित प्रदेश",
        "district_label": "ज़िला",
        "district_placeholder": "उदा. भोपाल, इंदौर, जयपुर, पटना",
        
        # Form Fields - Occupation & Income
        "occupation_label": "मुख्य व्यवसाय",
        "occ_student": "विद्यार्थी (छात्र / छात्रा)",
        "occ_farmer": "किसान / कृषि",
        "occ_entrepreneur": "उद्यमी / व्यापारी / MSME",
        "occ_salaried": "वेतनभोगी कर्मचारी (निजी / सरकारी)",
        "occ_self_employed": "स्वरोजगार / पेशेवर / फ्रीलांसर",
        "occ_daily_wage": "दैनिक वेतनभोगी / श्रमिक / कारीगर",
        "occ_unemployed": "बेरोजगार / नौकरी तलाशकर्ता",
        "occ_homemaker": "गृहणी",
        "occ_retired": "वरिष्ठ नागरिक / सेवानिवृत्त",
        "occ_other": "अन्य",
        
        "income_label": "वार्षिक पारिवारिक आय (₹)",
        "income_help": "आपके परिवार की कुल सकल वार्षिक आय।",
        "income_slab_label": "त्वरित आय सीमा",
        "income_below_1l": "₹1,00,000 से कम (BPL / अत्यंत कम आय)",
        "income_1l_2_5l": "₹1,00,000 - ₹2,50,000 (कम आय / EWS)",
        "income_2_5l_5l": "₹2,50,000 - ₹5,00,000 (निम्न मध्यम)",
        "income_5l_8l": "₹5,00,000 - ₹8,00,000 (मध्यम आय / EWS सीमा)",
        "income_above_8l": "₹8,00,000 से अधिक",
        
        "education_label": "उच्चतम शिक्षा का स्तर",
        "edu_below_10th": "10वीं से कम",
        "edu_10th": "10वीं उत्तीर्ण (मैट्रिक)",
        "edu_12th": "12वीं उत्तीर्ण (इंटरमीडिएट)",
        "edu_diploma": "डिप्लोमा / वोकेशनल / ITI",
        "edu_graduate": "स्नातक (Graduate)",
        "edu_post_graduate": "परास्नातक (Post Graduate)",
        "edu_doctorate": "पीएच.डी. / डॉक्टरेट",
        
        # Conditional - Student
        "student_section": "🎓 छात्र विवरण",
        "student_level_label": "वर्तमान अध्ययन स्तर",
        "student_level_ug": "स्नातक / कॉलेज (B.Tech, B.Sc, B.Com, MBBS)",
        "student_level_pg": "परास्नातक / मास्टर्स (M.Tech, M.Sc, MBA)",
        "student_level_school": "विद्यालय / स्कूल (कक्षा 9-12)",
        "student_level_phd": "पीएच.डी. / रिसर्च फेलोशिप",
        "student_level_diploma": "डिप्लोमा / आईटीआई (ITI)",
        "student_course_label": "पाठ्यक्रम / संकाय",
        "student_course_placeholder": "उदा. बी.टेक, बी.एससी कृषि, एमबीबीएस, बी.कॉम, 12वीं",
        "student_inst_label": "संस्थान का प्रकार",
        "inst_govt": "सरकारी संस्थान",
        "inst_aided": "शासकीय सहायता प्राप्त (Govt-Aided)",
        "inst_private": "निजी संस्थान (Private)",
        
        # Conditional - Farmer
        "farmer_section": "🌾 कृषक विवरण",
        "farmer_ownership_label": "भूमि स्वामित्व की स्थिति",
        "farmer_owner": "भूमि स्वामी (स्वयं की कृषि भूमि)",
        "farmer_tenant": "पट्टेदार किसान / बटाईदार",
        "farmer_laborer": "भूमिहीन कृषि मजदूर",
        "farmer_land_label": "कृषि भूमि का आकार",
        "land_marginal": "सीमांत (< 1 हेक्टेयर / 2.5 एकड़ से कम)",
        "land_small": "लघु (1 से 2 हेक्टेयर / 2.5 - 5 एकड़)",
        "land_medium_large": "मध्यम या बड़ा (> 2 हेक्टेयर / 5 एकड़ से अधिक)",
        "land_none": "कोई भूमि नहीं (भूमिहीन)",
        
        # Conditional - Entrepreneur
        "entrepreneur_section": "💼 व्यवसाय एवं उद्यम विवरण",
        "business_type_label": "व्यवसाय का क्षेत्र",
        "biz_manufacturing": "विनिर्माण / उत्पादन (Manufacturing)",
        "biz_services": "सेवाएं / IT / परामर्श (Services)",
        "biz_trading": "व्यापार / खुदरा / दुकानदार (Trading)",
        "biz_agri_allied": "कृषि संबंधित / खाद्य प्रसंस्करण",
        "biz_handicraft": "हथकरघा / हस्तशिल्प / कारीगर इकाई",
        "business_stage_label": "व्यवसाय का चरण",
        "biz_ideation": "योजना स्तर / नई शुरुआत (Ideation)",
        "biz_early": "प्रारंभिक चरण (< 2 वर्ष से कार्यरत)",
        "biz_established": "स्थापित / विस्तार (> 2 वर्ष)",
        
        # Social Category & Sensitive Information
        "social_category_label": "सामाजिक श्रेणी (वैकल्पिक)",
        "cat_general": "सामान्य / अनारक्षित (General)",
        "cat_obc": "अन्य पिछड़ा वर्ग (OBC)",
        "cat_sc": "अनुसूचित जाति (SC)",
        "cat_st": "अनुसूचित जनजाति (ST)",
        "cat_ews": "आर्थिक रूप से कमजोर (EWS)",
        "cat_minority": "अल्पसंख्यक समुदाय (Minority)",
        
        "disability_label": "दिव्यांगता स्थिति (वैकल्पिक)",
        "dis_none": "कोई नहीं",
        "dis_locomotor": "शारीरिक दिव्यांगता (≥ 40%)",
        "dis_visual": "दृष्टिबाधित / कम दृष्टि",
        "dis_hearing": "श्रवण बाधित / वाणी",
        "dis_intellectual": "बौद्धिक / बहु-दिव्यांगता",
        "dis_other": "अन्य बेंचमार्क दिव्यांगता",
        
        "marital_label": "वैवाहिक स्थिति (वैकल्पिक)",
        "mar_single": "अविवाहित",
        "mar_married": "विवाहित",
        "mar_widowed": "विधवा / विधुर",
        "mar_divorced": "तलाकशुदा / अलग",
        
        "sensitive_info_notice": "🔒 **हम यह क्यों पूछते हैं:** सामाजिक श्रेणी, आय और दिव्यांगता का विवरण केवल सरकारी आरक्षण, कल्याणकारी सब्सिडी और शुल्क छूट की पात्रता जांचने के लिए उपयोग किया जाता है। आपका डेटा सुरक्षित है।",
        
        # Buttons & Actions
        "btn_next": "अगला चरण →",
        "btn_back": "← पिछला",
        "btn_skip": "वैकल्पिक प्रश्न छोड़ें",
        "btn_complete": "प्रोफ़ाइल सहेजें और योजनाएं देखें 🎉",
        "btn_update": "प्रोफ़ाइल अपडेट करें और पुनः जांचें",
        "btn_cancel": "रद्द करें",
        "btn_refresh": "🔄 अनुशंसाएं ताज़ा करें",
        "btn_edit_profile": "✏️ प्रोफ़ाइल संपादित करें",
        "btn_ask_schemate": "💬 Schemate से इस योजना के बारे में पूछें",
        "btn_official_link": "🔗 आधिकारिक आवेदन पोर्टल",
        "btn_view_details": "📄 योजना का विस्तृत विवरण",
        "btn_go_to_chat": "💬 Schemate चैट पर जाएं",
        
        # Recommendations Dashboard
        "rec_title": "आपके लिए अनुशंसित सरकारी योजनाएं",
        "rec_subtitle": "आपकी सत्यापित प्रोफ़ाइल के आधार पर जांची गई योजनाएं।",
        "filter_all": "सभी योजनाएं",
        "filter_eligible": "✅ संभावित पात्र",
        "filter_verification": "⚠️ सत्यापन आवश्यक",
        "filter_not_eligible": "❌ पात्र नहीं",
        "badge_eligible": "संभावित पात्र",
        "badge_verification": "सत्यापन आवश्यक",
        "badge_not_eligible": "पात्र नहीं",
        "tag_central": "🏛️ केंद्रीय योजना",
        "tag_state": "📍 राज्य योजना",
        "why_matches_title": "🎯 यह योजना आपके लिए क्यों उपयुक्त है",
        "missing_info_title": "⚠️ आवश्यक जानकारी / दस्तावेज़ सत्यापन",
        "benefits_title": "🎁 मुख्य लाभ",
        "documents_title": "📋 आवश्यक दस्तावेज़",
        "official_sources_title": "🏛️ आधिकारिक स्रोत एवं विभाग",
        "empty_recommendations": "चयनित फ़िल्टर के अनुसार कोई योजना नहीं मिली।",
        "disclaimer_text": "⚠️ **अस्वीकरण:** ये अनुशंसाएं प्रकाशित सरकारी मानदंडों पर आधारित हैं। अंतिम पात्रता आवेदन के बाद संबंधित विभाग द्वारा दस्तावेज़ सत्यापन पर निर्भर करती है।",
        
        # Messages & Validation
        "val_age_required": "कृपया 1 से 120 के बीच मान्य आयु दर्ज करें।",
        "val_state_required": "कृपया अपना निवास राज्य चुनें।",
        "val_income_required": "कृपया अपनी वार्षिक पारिवारिक आय दर्ज करें।",
        "profile_saved_success": "प्रोफ़ाइल सफलतापूर्वक सहेजी गई! व्यक्तिगत योजनाएं जांची जा रही हैं...",

        # Saved Schemes
        "nav_saved_schemes": "⭐ मेरी सहेजी गई योजनाएं",
        "saved_title": "मेरी सहेजी गई योजनाएं",
        "saved_subtitle": "अपनी महत्वपूर्ण सरकारी योजनाओं पर नज़र रखें।",
        "saved_stat_total": "कुल सहेजी गई योजनाएं",
        "saved_stat_eligible": "संभावित पात्र",
        "saved_stat_verify": "सत्यापन आवश्यक",
        "saved_search_placeholder": "नाम या कीवर्ड से खोजें...",
        "saved_filter_all_types": "सभी प्रकार",
        "saved_filter_central": "केंद्रीय योजनाएं",
        "saved_filter_state": "राज्य योजनाएं",
        "saved_filter_all_cats": "सभी श्रेणियां",
        "saved_sort_recent": "हाल ही में सहेजी गई",
        "saved_sort_az": "योजना का नाम (A-Z)",
        "saved_empty_title": "अभी तक कोई योजना सहेजी नहीं गई",
        "saved_empty_subtitle": "सरकारी योजनाओं को देखें और जो आपको पसंद आएं उन्हें सहेजें।",
        "saved_btn_explore": "🔍 योजनाएं खोजें",
        "saved_btn_remove": "सहेजी सूची से हटाएं",
        "saved_btn_saved": "✓ सहेजी गई",
        "saved_btn_save": "⭐ योजना सहेजें",
        "saved_notes_title": "📝 व्यक्तिगत नोट्स",
        "saved_notes_placeholder": "अपने निजी नोट्स जोड़ें (जैसे: आय प्रमाण पत्र बनवाना है)...",
        "saved_notes_save": "नोट्स सहेजें",
        "saved_notes_saved_toast": "नोट्स सफलतापूर्वक अपडेट किए गए!",
        "saved_checklist_title": "📋 आवश्यक दस्तावेज़ चेकलिस्ट",
        "saved_checklist_empty": "कोई विशिष्ट दस्तावेज़ आवश्यकताएं सूचीबद्ध नहीं हैं।",
        "saved_toast_saved": "योजना आपकी सूची में सहेज ली गई!",
        "saved_toast_removed": "योजना सहेजी सूची से हटा दी गई।",
    },
    
    "hinglish": {
        # Navigation & Brand
        "app_title": "Schemate AI",
        "app_tagline": "Indian Government Schemes ke liye aapka AI Copilot",
        "nav_recommendations": "🎯 Recommended Schemes",
        "nav_chat": "💬 AI Chatbot",
        "nav_profile": "👤 Meri Profile",
        "nav_language": "🌐 Language",
        "logout": "🚪 Log Out",
        
        # Language Selection Screen
        "choose_language_title": "Choose Your Preferred Language",
        "choose_language_subtitle": "Apni pasandeeda language select karein personalized schemes discover karne ke liye.",
        "lang_en_name": "English",
        "lang_en_desc": "Simple English with official government terminology",
        "lang_hi_name": "हिंदी (Hindi)",
        "lang_hi_desc": "Saral aur spasht Hindi mein sampurna jankari",
        "lang_hinglish_name": "Hinglish",
        "lang_hinglish_desc": "Everyday Hindi in English script (Aasan Hinglish)",
        
        # Onboarding Flow
        "onboarding_title": "Personalized Scheme Eligibility Onboarding",
        "onboarding_subtitle": "Kuch aasan sawalon ke jawab dein taaki Schemate aapke liye eligible Central aur State schemes match kar sake.",
        "step_1": "1. Language",
        "step_2": "2. Basic Details",
        "step_3": "3. Rozgar aur Income",
        "step_4": "4. Category aur Specifics",
        "step_indicator": "Step {current} of {total}: {title}",
        
        # Form Fields - Basic
        "age_label": "Aapki Age (Years)",
        "age_help": "Schemes mein age limit criteria hota hai.",
        "dob_label": "Date of Birth (Optional)",
        "gender_label": "Gender",
        "gender_male": "Male (Purush)",
        "gender_female": "Female (Mahila)",
        "gender_transgender": "Transgender",
        "gender_other": "Prefer not to say",
        "state_label": "Aapka State / Union Territory",
        "district_label": "District (Jila)",
        "district_placeholder": "Jaise: Bhopal, Indore, Jaipur, Patna",
        
        # Form Fields - Occupation & Income
        "occupation_label": "Aapka Rozgar (Occupation)",
        "occ_student": "Student (Chhatra / Chhatra)",
        "occ_farmer": "Farmer / Kheti-Kisaani",
        "occ_entrepreneur": "Business Owner / Entrepreneur / MSME",
        "occ_salaried": "Salaried Employee (Govt / Private)",
        "occ_self_employed": "Self-Employed / Freelancer / Professional",
        "occ_daily_wage": "Daily Wage Worker / Majdoor / Karigar",
        "occ_unemployed": "Unemployed / Job Seeker",
        "occ_homemaker": "Homemaker (Grahani)",
        "occ_retired": "Senior Citizen / Retired",
        "occ_other": "Other",
        
        "income_label": "Varshik Parivarik Income (₹ Annual)",
        "income_help": "Aapki family ki total yearly gross income.",
        "income_slab_label": "Quick Income Slab",
        "income_below_1l": "₹1,00,000 se kam (BPL / Very Low)",
        "income_1l_2_5l": "₹1,00,000 - ₹2,50,000 (Low / EWS)",
        "income_2_5l_5l": "₹2,50,000 - ₹5,00,000 (Lower Middle)",
        "income_5l_8l": "₹5,00,000 - ₹8,00,000 (Middle / EWS Ceiling)",
        "income_above_8l": "Above ₹8,00,000",
        
        "education_label": "Education Level",
        "edu_below_10th": "10th se kam",
        "edu_10th": "10th Pass (Matriculation)",
        "edu_12th": "12th Pass (Intermediate)",
        "edu_diploma": "Diploma / ITI / Vocational",
        "edu_graduate": "Graduate / Bachelor's Degree",
        "edu_post_graduate": "Post Graduate / Master's Degree",
        "edu_doctorate": "Doctorate / Ph.D.",
        
        # Conditional - Student
        "student_section": "🎓 Student Details",
        "student_level_label": "Abhi kaunsi class/course mein hain?",
        "student_level_ug": "Undergraduate / College (B.Tech, B.Sc, B.Com, MBBS)",
        "student_level_pg": "Postgraduate / Masters (M.Tech, M.Sc, MBA)",
        "student_level_school": "School (Class 9-12)",
        "student_level_phd": "Ph.D. / Research Fellowship",
        "student_level_diploma": "Diploma / ITI",
        "student_course_label": "Course / Stream",
        "student_course_placeholder": "Jaise: B.Tech, B.Sc, MBBS, B.Com, 12th Board",
        "student_inst_label": "College / School ka type",
        "inst_govt": "Government Institute",
        "inst_aided": "Government Aided",
        "inst_private": "Private Institute",
        
        # Conditional - Farmer
        "farmer_section": "🌾 Farmer & Kheti Details",
        "farmer_ownership_label": "Zameen Ownership Status",
        "farmer_owner": "Apni kheti ki zameen hai (Landowner)",
        "farmer_tenant": "Batai / Rent par kheti (Tenant Farmer)",
        "farmer_laborer": "Bina zameen ke khet majdoor (Landless Laborer)",
        "farmer_land_label": "Zameen ka Size",
        "land_marginal": "Marginal (< 1 Hectare / < 2.5 Acres)",
        "land_small": "Small (1 to 2 Hectares / 2.5 - 5 Acres)",
        "land_medium_large": "Medium / Large (> 2 Hectares / > 5 Acres)",
        "land_none": "Zameen nahi hai (Landless)",
        
        # Conditional - Entrepreneur
        "entrepreneur_section": "💼 Business & Startup Details",
        "business_type_label": "Business Sector",
        "biz_manufacturing": "Manufacturing / Factory",
        "biz_services": "Services / IT / Repair",
        "biz_trading": "Trading / Retail / Dukan",
        "biz_agri_allied": "Agriculture Allied / Food Processing",
        "biz_handicraft": "Handloom / Handicraft Unit",
        "business_stage_label": "Business ka Stage",
        "biz_ideation": "Idea stage / Naya start karna hai",
        "biz_early": "Early Stage (< 2 saal se chal raha hai)",
        "biz_established": "Established (> 2 saal se chal raha hai)",
        
        # Social Category & Sensitive Information
        "social_category_label": "Social Category (Optional)",
        "cat_general": "General / Unreserved",
        "cat_obc": "OBC (Other Backward Class)",
        "cat_sc": "SC (Scheduled Caste)",
        "cat_st": "ST (Scheduled Tribe)",
        "cat_ews": "EWS (Economically Weaker Section)",
        "cat_minority": "Minority Community",
        
        "disability_label": "Divyangjan Status (Optional)",
        "dis_none": "None (Koi nahi)",
        "dis_locomotor": "Locomotor / Physical Disability (≥ 40%)",
        "dis_visual": "Visual / Aankhon se sambandhit",
        "dis_hearing": "Hearing / Bolne/Sunne mein",
        "dis_intellectual": "Intellectual / Multiple Disability",
        "dis_other": "Other Benchmark Disability",
        
        "marital_label": "Marital Status (Optional)",
        "mar_single": "Single / Unmarried",
        "mar_married": "Married",
        "mar_widowed": "Vidva / Widowed",
        "mar_divorced": "Divorced / Separated",
        
        "sensitive_info_notice": "🔒 **Yeh kyu chahiye:** Category, income aur disability info sirf government reservation, subsidies aur fee concessions ki eligibility check karne ke liye use hoti hai. Aapka data 100% private aur safe hai.",
        
        # Buttons & Actions
        "btn_next": "Next Step →",
        "btn_back": "← Back",
        "btn_skip": "Skip Optional Questions",
        "btn_complete": "Profile Save Karein & Schemes Dekhein 🎉",
        "btn_update": "Profile Update Karein & Refresh",
        "btn_cancel": "Cancel",
        "btn_refresh": "🔄 Recommendations Refresh Karein",
        "btn_edit_profile": "✏️ Profile Edit Karein",
        "btn_ask_schemate": "💬 Schemate se is scheme ke baare mein poochein",
        "btn_official_link": "🔗 Official Application Portal",
        "btn_view_details": "📄 Scheme Details Dekhein",
        "btn_go_to_chat": "💬 Schemate Chatbot Par Jayein",
        
        # Recommendations Dashboard
        "rec_title": "Your Recommended Government Schemes",
        "rec_subtitle": "Aapki verified profile details ke basis par evaluate ki gayi schemes.",
        "filter_all": "All Schemes",
        "filter_eligible": "✅ Potentially Eligible",
        "filter_verification": "⚠️ Needs Verification",
        "filter_not_eligible": "❌ Not Eligible",
        "badge_eligible": "Potentially Eligible",
        "badge_verification": "Needs Verification",
        "badge_not_eligible": "Not Eligible",
        "tag_central": "🏛️ Central Scheme",
        "tag_state": "📍 State Scheme",
        "why_matches_title": "🎯 Yeh scheme aapke liye kyu match hui",
        "missing_info_title": "⚠️ Missing Information / Verification Required",
        "benefits_title": "🎁 Key Benefits",
        "documents_title": "📋 Required Documents",
        "official_sources_title": "🏛️ Official Sources & Department",
        "empty_recommendations": "Chuni gayi category mein koi scheme nahi mili.",
        "disclaimer_text": "⚠️ **Disclaimer:** Yeh recommendations government rules ke aadhar par hain. Final approval application submit hone ke baad concerned department ke verification par depend karta hai.",
        
        # Messages & Validation
        "val_age_required": "Kripya 1 se 120 ke beech valid age dalein.",
        "val_state_required": "Kripya apna state select karein.",
        "val_income_required": "Kripya apni annual family income dalein.",
        "profile_saved_success": "Profile successfully save ho gayi! Schemes calculate ho rahi hain...",

        # Saved Schemes
        "nav_saved_schemes": "⭐ Meri Saved Schemes",
        "saved_title": "Meri Saved Schemes",
        "saved_subtitle": "Aapke liye important government schemes ko track karein.",
        "saved_stat_total": "Total Saved Schemes",
        "saved_stat_eligible": "Potentially Eligible",
        "saved_stat_verify": "Needs Verification",
        "saved_search_placeholder": "Name ya keyword se search karein...",
        "saved_filter_all_types": "All Types",
        "saved_filter_central": "Central Schemes",
        "saved_filter_state": "State Schemes",
        "saved_filter_all_cats": "All Categories",
        "saved_sort_recent": "Recently Saved",
        "saved_sort_az": "Scheme Name (A-Z)",
        "saved_empty_title": "Abhi tak koi scheme save nahi ki gayi",
        "saved_empty_subtitle": "Government schemes explore karein aur jo pasand aayein unhe save karein.",
        "saved_btn_explore": "🔍 Schemes Explore Karein",
        "saved_btn_remove": "Saved se Hatayein",
        "saved_btn_saved": "✓ Saved",
        "saved_btn_save": "⭐ Save Scheme",
        "saved_notes_title": "📝 Personal Notes",
        "saved_notes_placeholder": "Apne personal notes add karein (e.g. Income certificate submit karna hai)...",
        "saved_notes_save": "Notes Save Karein",
        "saved_notes_saved_toast": "Notes successfully update ho gaye!",
        "saved_checklist_title": "📋 Required Documents Checklist",
        "saved_checklist_empty": "Koi specific documents listed nahi hain.",
        "saved_toast_saved": "Scheme aapki saved list mein add ho gayi!",
        "saved_toast_removed": "Scheme saved list se hata di gayi.",
    }
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    """
    Get localized string for key and language code.
    Falls back to English if key is missing in chosen language.
    """
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    text = lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text


def localize_scheme_data(scheme: dict, lang: str = "en") -> dict:
    """Translates common reason templates, document labels, and text to Hindi/Hinglish if requested."""
    if lang != "hi" and lang != "hinglish":
        return scheme

    s = dict(scheme)
    
    # 1. Translate Match Reasons
    if s.get("match_reasons"):
        new_matches = []
        for r in s["match_reasons"]:
            if "Central Government Scheme" in r:
                new_matches.append("केंद्र सरकार की योजना (देश के सभी राज्यों एवं केंद्र शासित प्रदेशों में लागू)")
            elif "Resident of target state" in r:
                state_nm = r.split(":")[-1].strip()
                new_matches.append(f"पात्र राज्य के निवासी: {state_nm}")
            elif "Age" in r and "falls within" in r:
                new_matches.append(
                    r.replace("Age", "आयु")
                    .replace("yrs", "वर्ष")
                    .replace("falls within eligible bracket", "पात्र आयु वर्ग के भीतर है")
                    .replace("No upper limit", "कोई अधिकतम सीमा नहीं")
                )
            elif "Matches target occupation" in r:
                new_matches.append(
                    r.replace("Matches target occupation & group", "लक्षित व्यवसाय एवं वर्ग के अनुरूप")
                    .replace("Student", "विद्यार्थी")
                    .replace("Farmer", "किसान")
                    .replace("Entrepreneur", "व्यवसायी / उद्यमी")
                )
            elif "Family income" in r and "within permissible limit" in r:
                new_matches.append("पारिवारिक आय निर्धारित पात्रता सीमा के भीतर है")
            elif "Meets female beneficiary criteria" in r:
                new_matches.append("महिला लाभार्थी पात्रता मापदंड के पूर्णतः अनुकूल")
            elif "Institution type" in r:
                new_matches.append(r.replace("Institution type", "संस्थान का प्रकार"))
            else:
                new_matches.append(r)
        s["match_reasons"] = new_matches

    # 2. Translate Missing Criteria / Verification
    if s.get("missing_criteria"):
        new_missing = []
        for m in s["missing_criteria"]:
            if "Verification of original certificates" in m:
                new_missing.append("विभागीय दस्तावेज़ जांच के दौरान मूल प्रमाण पत्रों का सत्यापन")
            elif "Income certificate certifying" in m:
                new_missing.append("सक्षम प्राधिकारी द्वारा जारी आय प्रमाण पत्र")
            elif "Proof of age" in m:
                new_missing.append("आयु सत्यापन प्रमाण पत्र (जन्म प्रमाण पत्र / अंकसूची)")
            elif "Verification of domicile" in m:
                new_missing.append("मूल निवासी / अधिवास प्रमाण पत्र (Domicile Certificate)")
            else:
                new_missing.append(m)
        s["missing_criteria"] = new_missing

    # 3. Translate Required Documents
    doc_trans_hi = {
        "Aadhaar Card": "आधार कार्ड (Aadhaar Card)",
        "Proof of Identity": "पहचान पत्र (Proof of Identity)",
        "Bank Account Details / Passbook": "बैंक खाता विवरण / पासबुक",
        "Income Certificate": "आय प्रमाण पत्र (Income Certificate)",
        "Domicile Certificate": "मूल निवासी प्रमाण पत्र (Domicile)",
        "Caste Certificate": "जाति प्रमाण पत्र (Caste Certificate)",
        "Disability Certificate": "दिव्यांगता प्रमाण पत्र (Disability Cert)",
        "Passport Size Photographs": "पासपोर्ट साइज फोटो",
        "Ration Card": "राशन कार्ड (Ration Card)",
        "Educational Marksheet / Degree": "शैक्षणिक अंकसूची / प्रमाण पत्र",
        "Land Ownership Records (Khasra/Khatauni)": "भूमि खसरा / खतौनी दस्तावेज़",
    }
    if s.get("required_documents"):
        s["required_documents"] = [doc_trans_hi.get(d, d) for d in s["required_documents"]]

    return s



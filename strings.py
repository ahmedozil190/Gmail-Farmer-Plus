# Translation strings for Gmail Store Bot

STRINGS = {
    'ar': {
        'START_MSG_1': (
            "🎉 مرحباً بك في أسهل وأسرع طريقة للربح! 💰\n\n"
            "✨ ابدأ رحلتك نحو الربح الآن ✨"
        ),
        'START_MSG_2': "🎯 اختر زر تسجيل ايميل لتبدأ رحلتك! 🚀",
        
        # ── Force Join Channel ──
        'FORCE_JOIN_MSG': "📢 للاستخدام يجب الاشتراك أولاً في القناة الإجبارية:\n\n{channels}\n\n1) اضغط على زر الاشتراك\n2) اشترك في القناة\n3) ارجع واضغط \"تحقق من الاشتراك\"",
        'BTN_JOIN_CHANNEL': "اشترك في القناة 📢",
        'BTN_VERIFY_SUB': "تحقق من الاشتراك ✅",
        'ERR_NOT_JOINED': "لم تقم بالاشتراك في القناة بعد! ❌",
        
        # Main Menu Buttons
        'BTN_TASKS': "➕ تسجيل إيميل جديد",
        'BTN_MYACCOUNTS': "📂 حساباتي",
        'BTN_BALANCE': "💰 الرصيد",
        'BTN_REFERRAL': "👥 إحالاتي",
        'BTN_SETTINGS': "⚙️ الإعدادات",
        'BTN_CURRENCY': "💵 العملة",
        'BTN_LANG': "🌐 اللغة",
        'BTN_HELP': "💬 المساعدة",
        'BTN_BACK': "🔙 رجوع",
        
        # Balance Menu Buttons
        'BTN_PAYOUT': "💳 سحب",
        'BTN_HISTORY': "📜 سجل العمليات",
        
        # Balance
        'BALANCE_TITLE': "💰 <b>رصيدك</b>\n\n",
        'BALANCE_INFO_ONLY': (
            "الرصيد: <b>{balance:.2f}$</b>\n"
            "معلق: <b>{pending:.2f}$</b>\n"
        ),
        'BALANCE_INFO_DUAL': (
            "الرصيد: <b>{balance_text}</b>\n"
            "معلق: <b>{hold_text}</b>\n"
        ),
        'WALLET_STATS': "📊 <b>إحصائياتك</b>\n• حسابات مقبولة:  {approved}\n• حسابات مرفوضة: {rejected}",
        
        
        # Tasks
        'TASKS_TITLE': "📋 <b>المهام</b>\n\n",
        'TASKS_PRICE': "💵 السعر لكل حساب: <b>{price}</b>\n",
        'TASKS_STATS': "✅ حسابات مقبولة: <b>{approved}</b>\n⏳ في الانتظار: <b>{pending}</b>\n\n",
        'TASKS_PROMPT_EMAIL': "📨 أرسل لي عنوان Gmail الذي تريد بيعه\n<i>مثال: example@gmail.com</i>",
        'TASKS_ERROR_GMAIL': "⚠️ عنوان البريد الإلكتروني غير صحيح! يرجى إرسال Gmail صحيح (مثال: example@gmail.com)",
        'TASKS_PROMPT_PWD': "✅ تم استلام الإيميل: <code>{email}</code>\n\n🔑 الآن أرسل كلمة المرور للحساب:",
        'TASKS_SUCCESS': (
            "🎉 <b>تم إرسال الحساب بنجاح!</b>\n\n"
            "📧 الإيميل: <code>{email}</code>\n"
            "🔢 رقم الطلب: <b>#{sub_id}</b>\n\n"
            "⏳ سيتم مراجعة الحساب قريباً وإضافة {price_text} لمحفظتك عند القبول."
        ),
        'PROCESS_CANCELLED': "❌ تم إلغاء العملية.",
        'ERROR_RETRY': "❌ حدث خطأ، ابدأ من جديد.",
        
        # New Gmail Task Flow
        'BTN_METHOD_MANUAL': "📝 إنشاء يدوي - {price}",
        'BTN_METHOD_AUTO': "🤖 إنشاء تلقائي - {price}",
        'BTN_FOLLOW_UP': "✅ متابعة",
        'BTN_CANCEL': "❌ إلغاء",
        'MSG_CHOOSE_METHOD': "كيف تفضل إنشاء الحساب الجديد؟",
        'TASKS_PROMPT_EMAIL': (
            "✅ ممتاز! الآن أرسل عنوان الجيميل الذي أنشأته:\n\n"
            "💡 مثال: <code>yourname1234@gmail.com</code>\n\n"
            "⚠️ أرسل عنوان الجيميل فقط."
        ),
        'TASKS_MANUAL_INSTRUCTIONS': (
            "📱 <b>مهمة إنشاء جيميل</b> ⛳️\n\n"
            "📋 <b>التعليمات</b> 🥊\n\n"
            "🔑 كلمة المرور الموحدة ☜ <code>{unified_pwd}</code>\n\n"
            "📱 يجب إنشاء الحساب من الهاتف فقط\n\n"
            "👤 استخدم أي اسم أجنبي وبعده 3 او 4 ارقام 💁‍♂️\n\n"
            "📧 استخدم كلمة المرور الموحدة المذكورة أعلاه 🕺\n\n"
            "⚠️ ستحصل على المكافأة بعد موافقة الأدمن 💸\n\n"
            "💡 بعد إنشاء الحساب، اضغط \"متابعة\" لإدخال الإيميل 📲\n\n"
            "🕐 خذ وقتك - لا يوجد حد زمني لهذه المهمة ⏳"
        ),
        'MSG_AUTO_DATA': (
            "📱 <b>مهمة إنشاء جيميل جديدة - {price_text}</b>\n\n"
            "✨ اتبع الخطوات بهدوء وبالترتيب:\n\n"
            "1️⃣ اذهب إلى الإعدادات ثم المستخدمون والحسابات.\n\n"
            "2️⃣ اضغط إضافة حساب ثم اختر Google.\n\n"
            "3️⃣ اختر إنشاء حساب ثم لنفسي.\n\n"
            "4️⃣ أكتب الأسم الموجود بالأسفل واي تاريخ ميلاد.\n\n"
            "5️⃣ عند خطوة عنوان الجيميل استخدم هذا اليوزر:\n\n"
            "👤 <b>الاسم الأول:</b> <code>{first_name}</code>\n"
            "👤 <b>اسم العائلة:</b> <code>{last_name}</code>\n"
            "👤 <b>اليوزر:</b> <code>{username}</code>\n"
            "📧 <b>الشكل النهائي:</b> <code>{email}</code>\n"
            "🔑 <b>الباسورد:</b> <code>{password}</code>\n\n"
            "⚠️ كتابة باسورد مختلف قد يعرض حسابك للحظر ومنع سحب أرباحك.\n\n"
            "👇 بعد الانتهاء اختر واحدًا من الأزرار بالأسفل:"
        ),
        'BTN_AUTO_DONE': "✅ تم الانتهاء",
        'BTN_AUTO_REGEN': "🔄 تغيير البيانات",
        'BTN_AUTO_CANCEL': "❌ إلغاء التسجيل",
        'MSG_THANK_YOU_TRYING': (
            "🙏 شكراً للمحاولة\n\n"
            "📌 يمكنك طلب مهمة جديدة إن كانت متاحة.\n"
            "✨ حاول مرة ثانية بهدوء أو من جهاز آخر."
        ),
        'TASKS_MENU_PROMPT': (
            "📋 قائمة المهام المتاحة\n\n"
            "💰 اختر مهمة الآن وابدأ تحقيق الأرباح.\n"
            "⚡️ كلما أنجزت مهام أكثر زادت أرباحك.\n\n"
            "⏳ سيتم إضافة الأرباح إلى حسابك خلال 3 ايام كحد أقصى."
        ),
        'TASKS_PAUSED': (
            "🚧 <b>تنويه مهم</b>\n"
            "نظراً للإقبال الكبير على الخدمة حالياً، تم إيقاف إنشاء حسابات Gmail مؤقتاً لتنظيم الطلبات وضمان جودة الخدمة.\n\n"
            "🔔 سيتم إشعاركم تلقائياً فور عودة الخدمة.\n"
            "🙏 نشكر تفهّمكم وصبركم."
        ),
        'TASK_APPROVED': (
            "✅ تم قبول حسابك!\n\n"
            "📧 الحساب: {gmail}\n"
            "💰 تم إضافة {price} إلى رصيدك.\n\n"
            "شكراً لمجهودك، استمر في العمل! 🚀"
        ),
        'TASK_REJECTED': (
            "❌ تم رفض حساب الجيميل الخاص بك.\n\n"
            "📧 الجيميل: {gmail}\n\n"
            "💡 راجع تعليمات المهمة وحاول مرة أخرى."
        ),
        'BTN_TASK_GMAIL': "📱 مهمة إنشاء جيميل - {price}",
        'TASKS_INSTRUCTIONS': (
            "📱 <b>مهمة إنشاء جيميل</b> ⛳️\n\n"
            "📋 <b>التعليمات</b> 🥊\n\n"
            "🔑 كلمة المرور الموحدة ☜ <code>Aa612003@\u200e</code>\n\n"
            "📱 يجب إنشاء الحساب من الهاتف فقط\n"
            "👤 استخدم أي اسم أجنبي 💁‍♂️\n\n"
            "📧 استخدم كلمة المرور الموحدة المذكورة أعلاه 🕺\n\n"
            "⚠️ ستحصل على المكافأة بعد موافقة الأدمن 💸\n\n"
            "💡 بعد إنشاء الحساب، اضغط \"متابعة\" لإدخال الإيميل 📲\n\n"
            "🕐 خذ وقتك - لا يوجد حد زمني لهذه المهمة ⏳"
        ),
        'TASKS_STEPS': (
            "📱 <b>خطوات إكمال هذه المهمة:</b>\n\n"
            "1️⃣ أنشئ حساب جيميل باستخدام كلمة المرور أعلاه\n"
            "2️⃣ اضغط زر \"متابعة\" أدناه\n"
            "3️⃣ قم بتسجيل الخروج من الحساب\n"
            "4️⃣ أرسل عنوان الجيميل الجديد\n"
            "5️⃣ انتظر موافقة الأدمن\n\n"
            "💰 ستحصل على مكافأتك بعد الموافقة!\n\n"
            "❌ إذا لم تتمكن من إكمال المهمة، يرجى إلغاؤها"
        ),
        'TASKS_AUTO_INSTRUCTIONS': (
            "🤖 <b>تعليمات الإنشاء السريع</b>\n\n"
            "⚠️ يجب استخدام البيانات المولدة أدناه (الاسم، البريد، الباسورد) بالملي.\n"
            "⛔️ أي تغيير في البيانات سيؤدي لرفض الحساب تلقائياً.\n"
            "📱 تأكد من إنشاء الحساب من متصفح خفي أو هاتف نظيف."
        ),
        'TASKS_AUTO_STEPS': (
            "🚀 <b>خطوات الإنشاء السريع:</b>\n\n"
            "1️⃣ انسخ البيانات المولدة أدناه (الاسم والبريد والباسورد)\n"
            "2️⃣ افتح Gmail وأنشئ الحساب بهذه البيانات تماماً\n"
            "3️⃣ بعد الانتهاء، اضغط على زر [تأكيد الإنشاء السريع] بالأسفل\n"
            "4️⃣ انتظر مراجعة الحساب وإضافة الرصيد لمحفظتك"
        ),
        'TASKS_PROMPT_EMAIL_ONLY': (
            "✅ ممتاز! الآن أرسل عنوان الجيميل الذي أنشأته:\n\n"
            "💡 مثال: <code>yourname@gmail.com</code>\n\n"
            "⚠️ تأكد من إرسال عنوان الإيميل فقط!"
        ),
        'TASKS_SUCCESS_ONLY': (
            "✅ ممتاز! تم إرسال حساب الجيميل للمراجعة!\n\n"
            "💰 ستحصل على مكافأتك بعد موافقة الأدمن\n\n"
            "📞 إذا كان لديك أي استفسار، تواصل مع الدعم"
        ),
        'ERR_DUPLICATE_GMAIL': (
            "❌ تم إرسال هذا العنوان من قبل!\n\n"
            "💡 يرجى إنشاء حساب جيميل جديد وإرسال عنوان مختلف\n\n"
            "🔄 كل عنوان جيميل يمكن استخدامه مرة واحدة فقط\n\n"
            "أو اضغط إلغاء للخروج:"
        ),
        'BTN_CONTINUE': "متابعة ✅",
        'BTN_CANCEL_TASK': "إلغاء المهمة ❌",
        'MSG_TASK_CANCELLED': "✅ تم إلغاء المهمة",
        
        # Withdraw
        'WITHDRAW_LOW_BALANCE': (
            "❌ <b>رصيد غير كافٍ.</b> لا يمكنك طلب السحب في الوقت الحالي.\n\n"
            "{balance_info}\n\n"
            "يجب أن يكون رصيدك النشط أكبر من <b>$0</b> لطلب السحب."
        ),
        'WITHDRAW_TITLE': "📤 <b>طلب سحب</b>\n\n",
        'WITHDRAW_AVAIL': "💰 رصيدك المتاح: <b>{balance_text}</b>\n\n",
        'WITHDRAW_METHOD_PROMPT': "اختر طريقة الاستلام:",
        'WITHDRAW_AMOUNT_PROMPT': "✅ الطريقة: <b>{method}</b>\n\n💵 أدخل المبلغ المراد سحبه (الحد الأدنى {min_w:.2f}$، المتاح {balance:.2f}$):",
        'WITHDRAW_ERROR_NUM': "⚠️ أدخل رقمًا صحيحًا.",
        'WITHDRAW_ERROR_MIN': "⚠️ الحد الأدنى للسحب {min_w:.2f}$.",
        'WITHDRAW_ERROR_MAX': "⚠️ المبلغ يتجاوز رصيدك ({balance:.2f}$).",
        'WITHDRAW_WALLET_PROMPT': "📝 أدخل {label}:",
        'WITHDRAW_SUCCESS': "✅ <b>تم تقديم طلب السحب بنجاح!</b>\n\n💵 المبلغ: <b>{amount_text}</b>\n💰 الطريقة: <b>{method}</b>\n🏦 العنوان: <code>{wallet}</code>\n\nسيتم مراجعة طلبك وإرساله في أقرب وقت. شكراً لك!",
        'WITHDRAW_CONFIRM_BTN': "✅ تأكيد السحب",
        'WITHDRAW_EDIT_BTN': "✏️ تعديل",
        'WITHDRAW_PAID': (
            "🎉 <b>تم السحب بنجاح</b>\n\n"
            "✅ تم تحويل مبلغ <b>{amount_text}</b> بنجاح!\n"
            "💳 الطريقة: {method}\n"
            "🏦 العنوان: <code>{wallet}</code>\n\n"
            "شكراً لعملك معنا! استمر في الإنجاز 🚀"
        ),
        'WITHDRAW_REJECTED': (
            "❌ <b>تم رفض طلب السحب</b>\n\n"
            "للأسف تم رفض طلب السحب الخاص بك لمبلغ <b>{amount_text}</b>.\n"
            "🏦 العنوان: <code>{wallet}</code>\n\n"
            "🥊 لا تيأس! استمر في العمل لتحقيق المزيد من الأرباح 💰"
        ),
        
        # History & Accounts
        'HISTORY_EMPTY': "لا يوجد سجل عمليات حالياً.",
        'HISTORY_TITLE': "📜 <b>قائمة العمليات ({count})</b>\n\n",
        'MY_ACCOUNTS_TITLE': "📂 <b>قائمة حساباتي ({count})</b>\n",
        'MY_ACCOUNTS_EMPTY': "لا توجد حسابات مسجلة حالياً.",
        'MY_ACCOUNTS_ITEM_TEMPLATE': (
            "<b>الحالة:</b> {status}\n"
            "<b>الكود:</b> #{task_id}\n"
            "<b>الإيميل:</b> <code>{gmail}</code>\n"
            "<b>التاريخ:</b> {date}\n"
        ),
        'ST_APPROVED': "مقبول ✅",
        'ST_PENDING': "في الانتظار ⏳",
        'ST_REJECTED': "مرفوض ❌",
        'ST_PAID': "تم الدفع ✅",
        'ST_COMPLETED': "مكتمل ✅",
        'HISTORY_STATUS': "الحالة:",
        'HISTORY_METHOD': "الطريقة:",
        'HISTORY_PRICE': "المبلغ:",
        'HISTORY_ADDR': "العنوان:",
        'HISTORY_DATE': "التاريخ:",
        'DASH_PAY_ID': "رقم الدفع:",
        'HISTORY_ITEM_TEMPLATE': (
            "<b>{pay_id_lbl}</b> #{pay_id}\n"
            "<b>{status_lbl}</b> {status}\n"
            "<b>{method_lbl}</b> {method}\n"
            "<b>{price_lbl}</b> {price}\n"
            "<b>{addr_lbl}</b> {address}\n"
            "<b>{date_lbl}</b> {date}"
        ),
        'HISTORY_METHOD_SUBMISSION': "مهمة جيميل 📧",
        'SUPPORT_MSG': "💬 <b>المساعدة والدعم الفني</b>\n\nللتحدث مع الدعم الفني: {link}",

        # Wallet Labels
        'LBL_WALLET_VODAFONE': "رقم فودافون كاش",
        'LBL_WALLET_BINANCE': "Binance Pay ID أو UID",
        'LBL_WALLET_USDT': "عنوان محفظة USDT (BEP20)",
        'LBL_WALLET_TRX': "عنوان محفظة TRX (TRC20)",
        'LBL_WALLET_GENERIC': "عنوان المحفظة",
        
        # Referral
        'REF_MSG': (
            "📎 <b>نظام الإحالة</b>\n\n"
            "💰 احصل على {bonus_text} عن كل مهمة جيميل يكملها أصدقاؤك!\n\n"
            "📊 <b>إحصائياتك:</b>\n"
            "👥 الأصدقاء المدعوين: <b>{invited}</b>\n"
            "🎯 إجمالي المهام: <b>{tasks}</b>\n"
            "💰 إجمالي الأرباح: <b>{profit_text}</b>\n\n"
            "💡 أصدقاؤك يعملون = أنت تربح!\n"
            "✨ إمكانية ربح غير محدودة!"
        ),
        'REF_STATS_MSG': (
            "📊 <b>إحصائيات الإحالة:</b>\n\n"
            "👥 إجمالي المدعوين: <b>{invited}</b>\n"
            "✅ الإحالات النشطة: <b>{active}</b>\n"
            "🎯 إجمالي المهام المكتملة: <b>{tasks}</b>\n"
            "💰 إجمالي الأرباح: <b>{profit_text}</b>\n"
            "💵 المكافأة لكل مهمة: <b>{bonus_text}</b>\n\n"
            "🔗 كود الإحالة: <code>{ref_id}</code>\n\n"
            "💡 تحصل على {bonus_text} عن كل مهمة جيميل يكملها أصدقاؤك!\n"
            "✨ كلما عملوا أكثر، ربحت أكثر!"
        ),
        'REF_LINK_DETAILS': (
            "🔗 <b>رابط الإحالة الخاص بك:</b>\n\n"
            "{link}\n\n"
            "📋 انسخ هذا الرابط وشاركه مع أصدقائك\n"
            "💰 ستحصل على {bonus_text} عن كل مهمة جيميل يكملونها!\n\n"
            "🎯 كود الإحالة: <code>{ref_id}</code>\n\n"
            "💡 كلما أكملوا مهام أكثر، ربحت أكثر!\n"
            "✨ إمكانية ربح غير محدودة!\n\n"
            "👆 اضغط على الرابط أعلاه لتجربته!"
        ),
        'BTN_REF_LINK': "🔗 رابط الإحالة",
        'BTN_REF_STATS': "📊 إحصائيات الإحالة",
        'BTN_REF_LIST': "👥 قائمة الإحالات",
        'BTN_BACK_MAIN': "🔙 العودة للقائمة الرئيسية",
        'REF_LIST_EMPTY': (
            "👥 <b>قائمة الإحالات:</b>\n\n"
            "📭 لم تقم بإحالة أي شخص بعد\n\n"
            "💡 شارك رابط الإحالة لتبدأ الربح!"
        ),
        'REF_LIST_HEADER': "👥 <b>قائمة إحالاتك({count})</b>\n\n",
        'REF_LIST_ITEM': (
            "<b>{index}. المستخدم:</b> {name}\n"
            "<b>الحالة:</b> {status_text} {status_icon}\n"
            "<b>الأرباح:</b> {earned_text}\n"
            "<b>التاريخ:</b> {date}\n"
            "────────────────\n"
        ),
        'REF_STATUS_PENDING': "معلق",
        'REF_STATUS_EARNED': "تم الكسب",
        'REF_EARNED_NONE': "لم يتم الكسب بعد",
        
        # Admin Commands
        'ADMIN_ONLY': "⛔ هذا الأمر للأدمن فقط.",
        'ADMIN_PANEL_TITLE': "🛠 <b>لوحة التحكم</b>\n\n",
        'ADMIN_PANEL_STATS': (
            "👥 إجمالي المستخدمين:   <b>{total}</b>\n"
            "✅ حسابات مقبولة:      <b>{approved}</b>\n"
            "⏳ حسابات معلقة:       <b>{pending}</b>\n"
            "💸 طلبات سحب معلقة:    <b>{pending_w}</b>\n"
            "💰 إجمالي المدفوع:     <b>{paid_text}</b>\n\n"
            "الأوامر:\n"
            "/pending — الطلبات المعلقة\n"
            "/withdrawals — طلبات السحب\n"
            "/stats — إحصائيات مفصلة\n"
            "/broadcast رسالتك — إرسال للجميع"
        ),
        'ADMIN_PENDING_NONE': "✅ لا توجد طلبات معلقة.",
        'ADMIN_PENDING_HEADER': "📋 <b>الطلبات المعلقة ({count})</b>\n",
        'ADMIN_PENDING_ITEM': (
            "• <b>#{id}</b> | user:<code>{user_id}</code>\n"
            "  📧 <code>{gmail}</code>\n"
            "  🔑 <code>{pwd}</code>\n"
            "  📅 {date}\n"
            "  👉 /approve {id}  |  /reject {id} السبب"
        ),
        'ADMIN_APPROVE_USAGE': "استخدام: /approve <id>",
        'ADMIN_APPROVE_ERROR_ID': "⚠️ أدخل رقم طلب صحيح.",
        'ADMIN_APPROVE_NOT_FOUND': "❌ الطلب #{id} غير موجود أو تم معالجته مسبقاً.",
        'ADMIN_APPROVE_SUCCESS': (
            "✅ تم قبول الطلب <b>#{id}</b> ✅\n"
            "💰 تم إضافة المبلغ لمحفظة المستخدم."
        ),
        'ADMIN_REJECT_USAGE': "استخدام: /reject <id> [السبب]",
        'ADMIN_REJECT_SUCCESS': "🚫 تم رفض الطلب <b>#{id}</b>\nالسبب: {reason}",
        'ADMIN_W_PENDING_NONE': "✅ لا توجد طلبات سحب معلقة.",
        'ADMIN_W_PENDING_HEADER': "💸 <b>طلبات السحب المعلقة ({count})</b>\n",
        'ADMIN_W_PENDING_ITEM': (
            "• <b>#{id}</b> | user:<code>{user_id}</code>\n"
            "  💵 {amount_text}  |  {method}\n"
            "  🏦 <code>{wallet}</code>\n"
            "  👉 /paid {id}"
        ),
        'ADMIN_PAID_USAGE': "استخدام: /paid <id>",
        'ADMIN_PAID_SUCCESS': "✅ تم تأكيد السحب #{id} كمكتمل.",
        'ADMIN_STATS_TITLE': "📊 <b>الإحصائيات الكاملة</b>\n\n",
        'ADMIN_STATS_BODY': (
            "👥 المستخدمون: <b>{total}</b>\n"
            "✅ مقبول: <b>{approved}</b>\n"
            "⏳ معلق: <b>{pending}</b>\n"
            "💰 مدفوع: <b>{paid_text}</b>"
        ),
        'ADMIN_BROADCAST_USAGE': "استخدام: /broadcast رسالتك هنا",
        'ADMIN_BROADCAST_SUCCESS': "📢 <b>تم الإرسال</b>\n✅ نجح: {sent} | ❌ فشل: {failed}",
        'ADMIN_REJECT_W_USAGE': "❌ الاستخدام: /reject_w <الرقم> [السبب]",
        'ADMIN_REJECT_W_SUCCESS': "✅ تم رفض طلب السحب {id}. السبب: {reason}",
        
        # Admin Notifications (New Gmail/Withdraw)
        'ADMIN_NOTIFY_GMAIL': (
            "<b>الحالة:</b> {status}\n"
            "<b>رقم المهمة:</b> #{sub_id}\n"
            "<b>الجيميل:</b> <code>{gmail}</code>\n"
            "<b>كلمة المرور:</b> <code>{pwd}</code>\n"
            "<b>السعر:</b> {price}\n"
            "<b>التاريخ:</b> {date}\n"
            "<b>آيدي المستخدم:</b> <code>{user_id}</code>\n\n"
            "قبول: /approve {sub_id}\n"
            "رفض: /reject {sub_id}"
        ),
        'DASH_STATUS_LABEL': "الحالة (Status):",
        'DASH_PASS_LABEL': "Password:",
        'DASH_GMAIL_LABEL': "Gmail:",
        'DASH_PRICE_LABEL': "Price:",
        'DASH_DATE_LABEL': "Date:",
        'DASH_USER_LABEL': "User ID:",
        'DASH_FILTER_PENDING': "قيد الانتظار",
        'DASH_PENDING': "قيد الانتظار",
        'DASH_APPROVED': "مقبول",
        'DASH_REJECTED': "مرفوض",
        'ADMIN_NOTIFY_WITHDRAW': (
            "💸 <b>طلب سحب جديد ({source})</b>\n\n"
            "الرقم التعريفي: {wid}\n"
            "👤 اسم المستخدم: {user_name}\n"
            "👤 آيدي المستخدم: <code>{user_id}</code>\n"
            "💵 المبلغ: <b>{amount_text}</b>\n"
            "💳 الطريقة: {method}\n"
            "🏦 المحفظة: <code>{wallet}</code>\n\n"
            "تأكيد: /paid {wid}\n"
            "رفض: /reject_w {wid}"
        ),
        'NOTIFY_USER_APPROVE': (
            "🎉 <b>تهانينا!</b> تم قبول حسابك!\n\n"
            "📧 Gmail: <code>{gmail}</code>\n"
            "💵 تم إضافة <b>{price_text}</b> لمحفظتك ✅"
        ),
        'NOTIFY_USER_REJECT': (
            "❌ <b>تم رفض حسابك</b>\n\n"
            "📧 Gmail: <code>{gmail}</code>\n"
            "📝 السبب: {reason}\n\n"
            "يمكنك إرسال حساب آخر."
        ),
        'NOTIFY_USER_PAID': (
            "🎉 <b>دفع ناجح</b>\n\n"
            "✅ تم إرسال دفعتك بقيمة <b>{amount_text}</b> بنجاح!\n"
            "💳 الطريقة: {method}\n"
            "🏦 العنوان: <code>{wallet}</code>\n\n"
            "شكراً لعملك معنا! استمر 🚀"
        ),
        'LBL_CURRENCY_EGP': "جنيه",
        'DEF_REASON': "غير محدد",
        # Balance Menu Buttons
        'SETTINGS_MSG': "⚙️ <b>الإعدادات</b>\n\nاختر الخيار الذي تريد تعديله:",
        
        # Currency
        'CURRENCY_MSG': (
            "The main currency in the bot is <b>USD - US dollar</b>, however, you can choose "
            "one of the 174 currencies that will be used for visual display\n\n"
            "❗️ The currency you choose affects only the visual display, it can always be changed in settings"
        ),
        'CURRENCY_SET_SUCCESS': "✅ تم ضبط العملة بنجاح إلى: <b>{currency}</b>",
        'BTN_NEXT_PAGE': "➡️ الصفحة التالية",
        'BTN_PREV_PAGE': "⬅️ الصفحة السابقة",
        'BTN_NEXT_PAGE_INLINE': "التالي",
        'BTN_PREV_PAGE_INLINE': "السابق",
        
        'TASKS_AUTO_INSTRUCTIONS': (
            "🤖 <b>تعليمات الإنشاء السريع</b>\n\n"
            "⚠️ يجب عليك استخدام البيانات المولدة أدناه (الاسم، البريد الإلكتروني، كلمة المرور) بدقة.\n"
            "⛔️ أي اختلاف في البيانات سيؤدي إلى الرفض التلقائي.\n"
            "📱 تأكد من إنشاء الحساب من نافذة التصفح المتخفي أو جهاز نظيف."
        ),
        'TASKS_AUTO_STEPS': (
            "🚀 <b>خطوات الإنشاء السريع:</b>\n\n"
            "1️⃣ انسخ البيانات المولدة أدناه (الاسم، البريد الإلكتروني، كلمة المرور)\n"
            "2️⃣ افتح Gmail وأنشئ الحساب بهذه البيانات بالضبط\n"
            "3️⃣ بمجرد الانتهاء، اضغط على زر [تأكيد الإنشاء السريع] أدناه\n"
            "4️⃣ انتظر المراجعة وإضافة الرصيد إلى محفظتك"
        ),
        # Language
        'LANG_MSG': "🌐 اختر اللغة / Choose Language:",
    },
    'en': {
        'START_MSG_1': (
            "🎉 Welcome to the easiest and fastest way to earn! 💰\n\n"
            "✨ Start your journey to profit now ✨"
        ),
        'START_MSG_2': "🎯 Choose the Register Email button to start your journey! 🚀",
        
        # ── Force Join Channel ──
        'FORCE_JOIN_MSG': "📢 To use the bot, you must first subscribe to the mandatory channel:\n\n{channels}\n\n1) Click the join button\n2) Subscribe to the channel\n3) Return and click \"Verify Subscription\"",
        'BTN_JOIN_CHANNEL': "Join Channel 📢",
        'BTN_VERIFY_SUB': "Verify Subscription ✅",
        'ERR_NOT_JOINED': "You have not subscribed to the channel yet! ❌",
        
        # Main Menu Buttons
        'BTN_TASKS': "➕ Register a new Gmail",
        'BTN_MYACCOUNTS': "📂 My accounts",
        'BTN_BALANCE': "💰 Balance",
        'BTN_REFERRAL': "👥 My referrals",
        'BTN_SETTINGS': "⚙️ Settings",
        'BTN_CURRENCY': "💵 Currency",
        'BTN_LANG': "🌐 Language",
        'BTN_HELP': "💬 Help",
        'BTN_BACK': "🔙 Back",
        'LANG_MSG': "🌐 Choose your preferred language:\n\n🌐 اختر لغتك المفضلة:",
        
        # Balance Menu Buttons
        'BTN_PAYOUT': "💳 Payout",
        'BTN_HISTORY': "📜 Balance history",
        
        # Balance
        'BALANCE_TITLE': "💰 <b>Balance</b>\n\n",
        'BALANCE_INFO_ONLY': (
            "Balance: <b>{balance:.2f}$</b>\n"
            "Hold: <b>{pending:.2f}$</b>\n"
        ),
        'BALANCE_INFO_DUAL': (
            "Balance: <b>{balance_text}</b>\n"
            "Hold: <b>{hold_text}</b>\n"
        ),
        'WALLET_STATS': "📊 <b>Your Stats</b>\n• Approved accounts:  {approved}\n• Rejected accounts: {rejected}",
        
        
        # Tasks
        'TASKS_TITLE': "📋 <b>Tasks</b>\n\n",
        'TASKS_PRICE': "💵 Price per account: <b>{price}</b>\n",
        'TASKS_STATS': "✅ Approved: <b>{approved}</b>\n⏳ Pending: <b>{pending}</b>\n\n",
        'TASKS_PROMPT_EMAIL': "📨 Send me the Gmail address you want to sell\n<i>Example: example@gmail.com</i>",
        'TASKS_ERROR_GMAIL': "⚠️ Invalid email address! Please send a valid Gmail (e.g., example@gmail.com)",
        'TASKS_PROMPT_PWD': "✅ Email received: <code>{email}</code>\n\n🔑 Now send the account password:",
        'TASKS_SUCCESS': (
            "🎉 <b>Account submitted successfully!</b>\n\n"
            "📧 Email: <code>{email}</code>\n"
            "🔢 Order ID: <b>#{sub_id}</b>\n\n"
            "⏳ Account will be reviewed soon and {price_text} will be added to your wallet upon approval."
        ),
        'PROCESS_CANCELLED': "❌ Process cancelled.",
        'ERROR_RETRY': "❌ An error occurred, start over.",

        # New Gmail Task Flow
        'BTN_METHOD_MANUAL': "📝 Manual Creation - {price}",
        'BTN_METHOD_AUTO': "🤖 Auto-Generated - {price}",
        'BTN_FOLLOW_UP': "✅ Continue",
        'BTN_CANCEL': "❌ Cancel",
        'MSG_CHOOSE_METHOD': "How would you prefer to create the new account?",
        'TASKS_PROMPT_EMAIL': (
            "✅ Great! Now send the Gmail address you created:\n\n"
            "💡 Example: <code>yourname1234@gmail.com</code>\n\n"
            "⚠️ Send only the Gmail address."
        ),
        'TASKS_MANUAL_INSTRUCTIONS': (
            "📱 <b>Gmail Creation Task</b> ⛳️\n\n"
            "📋 <b>Instructions</b> 🥊\n\n"
            "🔑 Unified Password ☜ <code>{unified_pwd}</code>\n\n"
            "📱 Account must be created from phone only\n\n"
            "👤 Use any foreign name followed by 3 or 4 digits 💁‍♂️\n\n"
            "📧 Use the unified password mentioned above 🕺\n\n"
            "⚠️ You will receive the reward after admin approval 💸\n\n"
            "💡 After creating the account, press \"Continue\" to enter the email 📲\n\n"
            "🕐 Take your time - there is no time limit for this task ⏳"
        ),
        'MSG_AUTO_DATA': (
            "📱 <b>New Gmail Task - {price_text}</b>\n\n"
            "✨ Follow the steps calmly and in order:\n\n"
            "1️⃣ Go to Settings then Users & Accounts.\n\n"
            "2️⃣ Click Add Account then choose Google.\n\n"
            "3️⃣ Choose Create Account then For Myself.\n\n"
            "4️⃣ Write the name below and any birthday.\n\n"
            "5️⃣ At the Gmail address step use this username:\n\n"
            "👤 <b>First Name:</b> <code>{first_name}</code>\n"
            "👤 <b>Last Name:</b> <code>{last_name}</code>\n"
            "👤 <b>Username:</b> <code>{username}</code>\n"
            "📧 <b>Final Format:</b> <code>{email}</code>\n"
            "🔑 <b>Password:</b> <code>{password}</code>\n\n"
            "⚠️ Writing a different password may expose your account to a ban and prevent withdrawing your profits.\n\n"
            "👇 After finishing, choose one of the buttons below:"
        ),
        'BTN_AUTO_DONE': "✅ Done",
        'BTN_AUTO_REGEN': "🔄 Change Data",
        'BTN_AUTO_CANCEL': "❌ Cancel Registration",
        'MSG_THANK_YOU_TRYING': (
            "🙏 Thanks for trying\n\n"
            "📌 You can request a new task if available.\n"
            "✨ Try again calmly or from another device."
        ),
        'TASKS_MENU_PROMPT': (
            "📋 Available Tasks List\n\n"
            "💰 Choose a task now and start earning.\n"
            "⚡️ The more tasks you complete, the more you win.\n"
            "⏳ Profits will be added to your account within a maximum of 3 days."
        ),
        'TASKS_PAUSED': (
            "🚧 <b>Important Notice</b>\n"
            "Due to high demand, the creation of Gmail accounts has been temporarily paused to organize requests and ensure service quality.\n\n"
            "🔔 You will be notified automatically once the service resumes.\n"
            "🙏 Thank you for your understanding and patience."
        ),
        'TASK_APPROVED': (
            "✅ Your account has been approved!\n\n"
            "📧 Account: {gmail}\n"
            "💰 {price} has been added to your balance.\n\n"
            "Thank you for your effort, keep it up! 🚀"
        ),
        'TASK_REJECTED': (
            "❌ Your Gmail account has been rejected.\n\n"
            "📧 Gmail: {gmail}\n\n"
            "💡 Review the task instructions and try again."
        ),
        'BTN_TASK_GMAIL': "📱 Create Gmail Task - {price}",
        'TASKS_INSTRUCTIONS': (
            "📱 <b>Gmail Creation Task</b> ⛳️\n\n"
            "📋 <b>Instructions</b> 🥊\n\n"
            "🔑 Unified Password ☜ <code>Aa612003@</code>\n\n"
            "📱 Account must be created from phone only\n"
            "👤 Use any foreign name 💁‍♂️\n\n"
            "📧 Use the unified password mentioned above 🕺\n\n"
            "⚠️ You will receive the reward after admin approval 💸\n\n"
            "💡 After creating the account, press \"Continue\" to enter the email 📲\n\n"
            "🕐 Take your time - there is no time limit for this task ⏳"
        ),
        'TASKS_STEPS': (
            "📱 <b>Steps to complete this task:</b>\n\n"
            "1️⃣ Create a Gmail account using the password above\n"
            "2️⃣ Press the \"Continue\" button below\n"
            "3️⃣ Send the new Gmail address\n"
            "4️⃣ Wait for admin approval\n\n"
            "💰 You will get your reward after approval!\n\n"
            "❌ If you cannot complete the task, please cancel it"
        ),
        'TASKS_PROMPT_EMAIL_ONLY': (
            "✅ Excellent! Now send the Gmail address you created:\n\n"
            "💡 Example: <code>yourname@gmail.com</code>\n\n"
            "⚠️ Make sure to send the email address only!"
        ),
        'TASKS_SUCCESS_ONLY': (
            "✅ Excellent! The Gmail account has been submitted for review!\n\n"
            "💰 You will receive your reward after admin approval\n\n"
            "📞 If you have any questions, contact support"
        ),
        'ERR_DUPLICATE_GMAIL': (
            "❌ This address has already been submitted!\n\n"
            "💡 Please create a new Gmail account and send a different address\n\n"
            "🔄 Each Gmail address can be used only once\n\n"
            "Or press Cancel to exit:"
        ),
        'BTN_CONTINUE': "Continue ✅",
        'BTN_CANCEL_TASK': "Cancel Task ❌",
        'MSG_TASK_CANCELLED': "✅ Task cancelled",
        
        # Withdraw
        'WITHDRAW_LOW_BALANCE': (
            "❌ <b>Insufficient active balance.</b> You cannot request a payout at this time.\n\n"
            "{balance_info}\n\n"
            "Your active balance must be greater than <b>$0</b> to request a withdrawal."
        ),
        'WITHDRAW_TITLE': "📤 <b>Withdrawal Request</b>\n\n",
        'WITHDRAW_AVAIL': "💰 Available Balance: <b>{balance_text}</b>\n\n",
        'WITHDRAW_METHOD_PROMPT': "Choose payment method:",
        'WITHDRAW_AMOUNT_PROMPT': "✅ Method: <b>{method}</b>\n\n💵 Enter the amount to withdraw (Min {min_w:.2f}$, Available {balance:.2f}$):",
        'WITHDRAW_ERROR_NUM': "⚠️ Enter a valid number.",
        'WITHDRAW_ERROR_MIN': "⚠️ Minimum withdrawal is {min_w:.2f}$.",
        'WITHDRAW_ERROR_MAX': "⚠️ Amount exceeds your balance ({balance:.2f}$).",
        'WITHDRAW_WALLET_PROMPT': "📝 Enter your {label}:",
        'WITHDRAW_SUCCESS': "✅ <b>Withdrawal request submitted!</b>\n\n💵 Amount: <b>{amount_text}</b>\n💰 Method: <b>{method}</b>\n🏦 Address: <code>{wallet}</code>\n\nYour request will be reviewed and sent shortly. Thank you!",
        'WITHDRAW_CONFIRM_BTN': "✅ Confirm Withdrawal",
        'WITHDRAW_EDIT_BTN': "✏️ Edit",
        'WITHDRAW_PAID': (
            "🎉 <b>Payout Success</b>\n\n"
            "✅ Your payout of <b>{amount_text}</b> has been sent successfully!\n"
            "💳 Method: {method}\n"
            "🏦 Address: <code>{wallet}</code>\n\n"
            "Thank you for working with us! Keep it up 🚀"
        ),
        'WITHDRAW_REJECTED': (
            "❌ <b>Withdrawal Request Rejected</b>\n\n"
            "Unfortunately, your withdrawal request for <b>{amount_text}</b> was rejected.\n"
            "🏦 Address: <code>{wallet}</code>\n\n"
            "🥊 Don't give up! Keep working to earn more profits 💰"
        ),

        # History & Accounts
        'HISTORY_EMPTY': "No balance history yet.",
        'HISTORY_TITLE': "📜 <b>Balance History ({count})</b>\n\n",
        'MY_ACCOUNTS_TITLE': "📂 <b>My accounts ({count})</b>\n",
        'MY_ACCOUNTS_EMPTY': "No accounts registered yet.",
        'MY_ACCOUNTS_ITEM_TEMPLATE': (
            "<b>Status:</b> {status}\n"
            "<b>Task ID:</b> #{task_id}\n"
            "<b>Gmail:</b> <code>{gmail}</code>\n"
            "<b>Date:</b> {date}\n"
        ),
        'ST_APPROVED': "Approved ✅",
        'ST_PENDING': "Pending ⏳",
        'ST_REJECTED': "Rejected ❌",
        'ST_PAID': "Paid ✅",
        'ST_COMPLETED': "Completed ✅",
        'HISTORY_STATUS': "Status:",
        'HISTORY_METHOD': "Method:",
        'HISTORY_PRICE': "Price:",
        'HISTORY_ADDR': "Address:",
        'HISTORY_DATE': "Date:",
        'DASH_PAY_ID': "Pay ID:",
        'HISTORY_ITEM_TEMPLATE': (
            "<b>{pay_id_lbl}</b> #{pay_id}\n"
            "<b>{status_lbl}</b> {status}\n"
            "<b>{method_lbl}</b> {method}\n"
            "<b>{price_lbl}</b> {price}\n"
            "<b>{addr_lbl}</b> {address}\n"
            "<b>{date_lbl}</b> {date}"
        ),
        'HISTORY_METHOD_SUBMISSION': "Gmail Task 📧",
        'SUPPORT_MSG': "💬 <b>Help & Tech Support</b>\n\nTo contact support: {link}",

        # Wallet Labels
        'LBL_WALLET_VODAFONE': "Vodafone Cash Number",
        'LBL_WALLET_BINANCE': "Binance Pay ID or UID",
        'LBL_WALLET_USDT': "USDT (BEP20) Wallet Address",
        'LBL_WALLET_TRX': "TRX (TRC20) Wallet Address",
        'LBL_WALLET_GENERIC': "Wallet Address",
        
        # Referral
        'REF_MSG': (
            "📎 <b>Referral System</b>\n\n"
            "💰 Get {bonus_text} for every Gmail task completed by your referred friends!\n\n"
            "📊 <b>Your Stats:</b>\n"
            "👥 Invited friends: <b>{invited}</b>\n"
            "🎯 Total tasks: <b>{tasks}</b>\n"
            "💰 Total profit: <b>{profit_text}</b>\n\n"
            "💡 Your friends work = You earn!\n"
            "✨ Unlimited earning potential!"
        ),
        'REF_STATS_MSG': (
            "📊 <b>Referral Stats:</b>\n\n"
            "👥 Total invited: <b>{invited}</b>\n"
            "✅ Active referrals: <b>{active}</b>\n"
            "🎯 Total tasks completed: <b>{tasks}</b>\n"
            "💰 Total profit: <b>{profit_text}</b>\n"
            "💵 Bonus per task: <b>{bonus_text}</b>\n\n"
            "🔗 Referral code: <code>{ref_id}</code>\n\n"
            "💡 You get {bonus_text} for every Gmail task your friends complete!\n"
            "✨ The more they work, the more you win!"
        ),
        'REF_LINK_DETAILS': (
            "🔗 <b>Your Referral Link:</b>\n\n"
            "{link}\n\n"
            "📋 Copy this link and share it with your friends\n"
            "💰 You'll get {bonus_text} for every Gmail task they complete!\n\n"
            "🎯 Referral Code: <code>{ref_id}</code>\n\n"
            "💡 The more tasks they complete, the more you win!\n"
            "✨ Unlimited earning potential!\n\n"
            "👆 Click the link above to test it!"
        ),
        'BTN_REF_LINK': "🔗 Referral Link",
        'BTN_REF_STATS': "📊 Referral Stats",
        'BTN_REF_LIST': "👥 Referral List",
        'BTN_BACK_MAIN': "🔙 Back to Main Menu",
        'REF_LIST_EMPTY': (
            "👥 <b>Referral List:</b>\n\n"
            "📭 You haven't referred anyone yet\n\n"
            "💡 Share your referral link to start earning!"
        ),
        'REF_LIST_HEADER': "👥 <b>Your Referrals ({count})</b>\n\n",
        'REF_LIST_ITEM': (
            "<b>{index}. Username:</b> {name}\n"
            "<b>Status:</b> {status_text} {status_icon}\n"
            "<b>Earning:</b> {earned_text}\n"
            "<b>Date:</b> {date}\n"
            "────────────────\n"
        ),
        'REF_STATUS_PENDING': "Pending",
        'REF_STATUS_EARNED': "Earned",
        'REF_EARNED_NONE': "No profit yet",

        # Admin Commands
        'ADMIN_ONLY': "⛔ This command is for admin only.",
        'ADMIN_PANEL_TITLE': "🛠 <b>Admin Panel</b>\n\n",
        'ADMIN_PANEL_STATS': (
            "👥 Total Users:   <b>{total}</b>\n"
            "✅ Approved Tasks:      <b>{approved}</b>\n"
            "⏳ Pending Tasks:       <b>{pending}</b>\n"
            "💸 Pending Withdrawals:    <b>{pending_w}</b>\n"
            "💰 Total Paid:     <b>{paid_text}</b>\n\n"
            "Commands:\n"
            "/pending — Pending tasks\n"
            "/withdrawals — Withdrawal requests\n"
            "/stats — Detailed stats\n"
            "/broadcast your message — Send to all users"
        ),
        'ADMIN_PENDING_NONE': "✅ No pending tasks.",
        'ADMIN_PENDING_HEADER': "📋 <b>Pending Tasks ({count})</b>\n",
        'ADMIN_PENDING_ITEM': (
            "• <b>#{id}</b> | user:<code>{user_id}</code>\n"
            "  📧 <code>{gmail}</code>\n"
            "  🔑 <code>{pwd}</code>\n"
            "  📅 {date}\n"
            "  👉 /approve {id}  |  /reject {id} reason"
        ),
        'ADMIN_APPROVE_USAGE': "Usage: /approve <id>",
        'ADMIN_APPROVE_ERROR_ID': "⚠️ Enter a valid ID.",
        'ADMIN_APPROVE_NOT_FOUND': "❌ Task #{id} not found or already processed.",
        'ADMIN_APPROVE_SUCCESS': (
            "✅ Task <b>#{id}</b> approved ✅\n"
            "💰 Amount added to user's wallet."
        ),
        'ADMIN_REJECT_USAGE': "Usage: /reject <id> [reason]",
        'ADMIN_REJECT_SUCCESS': "🚫 Task <b>#{id}</b> rejected\nReason: {reason}",
        'ADMIN_W_PENDING_NONE': "✅ No pending withdrawals.",
        'ADMIN_W_PENDING_HEADER': "💸 <b>Pending Withdrawals ({count})</b>\n",
        'ADMIN_W_PENDING_ITEM': (
            "• <b>#{id}</b> | user:<code>{user_id}</code>\n"
            "  💵 {amount_text}  |  {method}\n"
            "  🏦 <code>{wallet}</code>\n"
            "  👉 /paid {id}"
        ),
        'ADMIN_PAID_USAGE': "Usage: /paid <id>",
        'ADMIN_PAID_SUCCESS': "✅ Withdrawal #{id} marked as paid.",
        'ADMIN_STATS_TITLE': "📊 <b>Global Statistics</b>\n\n",
        'ADMIN_STATS_BODY': (
            "👥 Users: <b>{total}</b>\n"
            "✅ Approved: <b>{approved}</b>\n"
            "⏳ Pending: <b>{pending}</b>\n"
            "💰 Paid: <b>{paid_text}</b>"
        ),
        'ADMIN_BROADCAST_USAGE': "Usage: /broadcast your message here",
        'ADMIN_BROADCAST_SUCCESS': "📢 <b>Broadcast Sent</b>\n✅ Success: {sent} | ❌ Failed: {failed}",
        'ADMIN_REJECT_W_USAGE': "❌ Usage: /reject_w <id> [reason]",
        'ADMIN_REJECT_W_SUCCESS': "✅ Withdrawal {id} rejected. Reason: {reason}",

        # Admin Notifications (New Gmail/Withdraw)
        'ADMIN_NOTIFY_GMAIL': (
            "<b>Status:</b> {status}\n"
            "<b>Task ID:</b> #{sub_id}\n"
            "<b>Gmail:</b> <code>{gmail}</code>\n"
            "<b>Password:</b> <code>{pwd}</code>\n"
            "<b>Price:</b> {price}\n"
            "<b>Date:</b> {date}\n"
            "<b>User ID:</b> <code>{user_id}</code>\n\n"
            "Approve: /approve {sub_id}\n"
            "Reject: /reject {sub_id}"
        ),
        'DASH_STATUS_LABEL': "Status:",
        'DASH_PASS_LABEL': "Password:",
        'DASH_GMAIL_LABEL': "Gmail:",
        'DASH_PRICE_LABEL': "Price:",
        'DASH_DATE_LABEL': "Date:",
        'DASH_USER_LABEL': "User ID:",
        'DASH_FILTER_PENDING': "Pending",
        'DASH_PENDING': "Pending",
        'DASH_APPROVED': "Approved",
        'DASH_REJECTED': "Rejected",
        'ADMIN_NOTIFY_WITHDRAW': (
            "💸 <b>New Withdrawal ({source})</b>\n\n"
            "Payment ID: {wid}\n"
            "👤 Username: {user_name}\n"
            "👤 User ID: <code>{user_id}</code>\n"
            "💵 Amount: <b>{amount_text}</b>\n"
            "💳 Method: {method}\n"
            "🏦 Address: <code>{wallet}</code>\n\n"
            "Confirm: /paid {wid}\n"
            "Reject: /reject_w {wid}"
        ),
        'NOTIFY_USER_APPROVE': (
            "🎉 <b>Congratulations!</b> Your account was accepted!\n\n"
            "📧 Gmail: <code>{gmail}</code>\n"
            "💵 <b>{price_text}</b> has been added to your wallet ✅"
        ),
        'NOTIFY_USER_REJECT': (
            "❌ <b>Your submission was rejected</b>\n\n"
            "📧 Gmail: <code>{gmail}</code>\n"
            "📝 Reason: {reason}\n\n"
            "You can submit another account."
        ),
        'NOTIFY_USER_PAID': (
            "🎉 <b>Payout Success</b>\n\n"
            "✅ Your payout of <b>{amount_text}</b> has been sent successfully!\n"
            "💳 Method: {method}\n"
            "🏦 Address: <code>{wallet}</code>\n\n"
            "Thank you for working with us! Keep it up 🚀"
        ),
        'LBL_CURRENCY_EGP': "EGP",
        'DEF_REASON': "Not specified",
        
        # Balance Menu Buttons
        'SETTINGS_MSG': "⚙️ <b>Settings</b>\n\nChoose the option you want to modify:",
        
        # Currency
        'CURRENCY_MSG': (
            "The main currency in the bot is <b>USD - US dollar</b>, however, you can choose "
            "one of the 174 currencies that will be used for visual display\n\n"
            "❗️ The currency you choose affects only the visual display, it can always be changed in settings"
        ),
        'CURRENCY_SET_SUCCESS': "✅ Currency successfully set to: <b>{currency}</b>",
        'BTN_NEXT_PAGE': "➡️ Next Page",
        'BTN_PREV_PAGE': "⬅️ Previous Page",
        'BTN_NEXT_PAGE_INLINE': "Next",
        'BTN_PREV_PAGE_INLINE': "Back",
        
        # Language
    },
}

WEBAPP_STRINGS = {
    'ar': {
        'NAV_HOME': "الرئيسية",
        'NAV_TASKS': "المهام",
        'NAV_WALLET': "المحفظة",
        'NAV_REFERRALS': "الإحالات",
        'BTN_PREV_PAGE_INLINE': "رجوع",
        
        'BANNED_TITLE': "✋ تم حظرك",
        'BANNED_MSG': "❌ <b>عذراً، تم حظرك من استخدام النظام.</b>\nلقد تم تقييد وصولك إلى لوحة التحكم بسبب مخالفة القوانين.",
        
        'HOME_WELCOME': "مرحباً بك مجدداً 👋",
        'HOME_GREETING': "نحن سعداء برؤيتك مرة أخرى",
        'HOME_BALANCE': "الرصيد المتاح",
        'HOME_CURRENT_BALANCE': "الرصيد الحالي",
        'HOME_TOTAL_WITHDRAWN': "إجمالي المسحوبات",
        'HOME_PENDING': "⏳ معلق: $%.2f",
        'HOME_USD': "دولار",
        'HOME_QUICK_ACTIONS': "إجراءات سريعة",
        'HOME_NEW_TASK': "مهمة جديدة",
        'HOME_EARN_REWARDS': "ابدأ في ربح المكافآت",
        'HOME_WITHDRAW': "سحب",
        'HOME_MANAGE_FUNDS': "إدارة أموالك",
        'HOME_INVITE': "دعوة",
        'HOME_INVITE_EARN': "ادعُ واربح",
        'HOME_SECURE': "آمن",
        'HOME_ENCRYPTED': "مشفر تماماً",
        'HOME_STATS': "📊 إحصائياتك",
        'HOME_APPROVED': "مقبول",
        'HOME_REJECTED': "مرفوض",
        'HOME_REQ_PENDING': "معلق",
        'HOME_RECENT_TASKS': "📋 آخر المهام",
        'HOME_VIEW_ALL': "عرض الكل ←",
        
        'TASKS_TITLE': "📱 المهام",
        'TASKS_CREATE_GMAIL': "إنشاء حساب Gmail",
        'TASKS_EARN': "اربح <b>$%.2f</b> لكل حساب",
        'TASKS_SUBTITLE_EARN': "ابدأ الآن بجني الأرباح عبر إنشاء حساب جيميل جديد بضغطة زر واحدة. 🚀",
        'TASKS_START': "ابدأ مهمة جديدة",
        'TASKS_PAUSED': "🚧 إنشاء المهام متوقف مؤقتاً. سيتم إخطارك عند العودة.",
        'TASKS_HISTORY': "📋 سجل التقديمات",
        'TASKS_EMPTY': "لا توجد مهام حالياً.<br>ابدأ بالربح عبر إنشاء حسابات Gmail!",
        'TASKS_REJECTED_HINT': "راجع تعليمات المهمة وحاول مرة أخرى.",
        
        'TASK_START_TITLE': "📱 مهمة Gmail جديدة",
        'TASK_START_INSTRUCTIONS': "📋 التعليمات",
        'TASK_START_PWD': "🔑 <b>كلمة المرور الموحدة:</b> <code class='copyable'>{}</code>",
        'TASK_START_RULE1': "📱 أنشئ الحساب من هاتفك فقط",
        'TASK_START_RULE2': "👤 استخدم أي اسم أجنبي",
        'TASK_START_RULE3': "📧 استخدم كلمة المرور الموحدة أعلاه",
        'TASK_START_RULE4': "⚠️ ستحصل على المكافأة بعد موافقة الأدمن",
        'TASK_START_RULE5': "🕐 خذ وقتك — لا يوجد حد زمني",
        'TASK_START_STEPS': "📝 الخطوات",
        'TASK_START_STEP1': "1️⃣ أنشئ حساب Gmail بكلمة المرور أعلاه",
        'TASK_START_STEP2': "2️⃣ أدخل عنوان Gmail الجديد بالأسفل",
        'TASK_START_STEP_3': '3️⃣ بمجرد الانتهاء، قم بإرسال الإيميل فقط هنا.',
        'TASK_START_STEP4': "4️⃣ انتظر موافقة الأدمن",
        'TASK_START_SUBMIT_LBL': "📧 أدخل بريد Gmail",
        'TASK_START_SUBMIT_PH': "أدخل عنوان الإيميل هنا...",
        'TASK_START_SUBMIT_BTN': "تقديم المهمة",
        'TASK_START_BACK': "العودة للمهام",
        'TASKS_MANUAL_MSG': (
            "📱 <b>مهمة إنشاء جيميل ⛳️</b>\n\n"
            "📋 <b>التعليمات 🥊</b>\n\n"
            "🔑 كلمة المرور الموحدة ☜ <code>{password}</code>\n\n"
            "📱 يجب إنشاء الحساب من الهاتف فقط\n\n"
            "👤 استخدم أي اسم أجنبي وبعده 3 او 4 ارقام 💁‍♂️\n\n"
            "📧 استخدم كلمة المرور الموحدة المذكورة أعلاه 🕺\n\n"
            "⚠️ ستحصل على المكافأة بعد موافقة الأدمن 💸\n\n"
            "💡 بعد إنشاء الحساب، أدخل الإيميل بالأسفل 📲\n\n"
            "🕐 خذ وقتك - لا يوجد حد زمني لهذه المهمة ⏳"
        ),
        
        'TASK_TAB_MANUAL': "إنشاء يدوي",
        'TASK_TAB_AUTO': "إنشاء تلقائي",
        'BTN_METHOD_MANUAL': "يدوي - {manual_price_text}",
        'BTN_METHOD_AUTO': "تلقائي - {auto_price_text}",
        'TASK_AUTO_INFO': "",
        'TASK_AUTO_FNAME': "الاسم الأول:",
        'TASK_AUTO_LNAME': "اسم العائلة:",
        'TASK_AUTO_EMAIL': "اليوزر:",
        'TASK_AUTO_PWD': "كلمة المرور:",
        'TASK_AUTO_BTN': "تم الانتهاء",
        'TASK_AUTO_REGEN': "تغيير البيانات",
        'TASK_AUTO_CANCEL': "❌  إلغاء التسجيل",
        'TASK_AUTO_WARNING': "⚠️ كتابة باسورد مختلف قد يعرض حسابك للحظر ومنع سحب أرباحك.",
        'TASK_AUTO_FOOTER': "👇 بعد الانتهاء اختر واحدًا من الأزرار بالأسفل:",
        'TASKS_AUTO_INSTRUCTIONS': (
            "📱 <b>مهمة إنشاء جيميل جديدة</b>\n\n"
            "✨ اتبع الخطوات بهدوء وبالترتيب:\n\n"
            "1️⃣ اذهب إلى الإعدادات ثم المستخدمون والحسابات.\n\n"
            "2️⃣ اضغط إضافة حساب ثم اختر Google.\n\n"
            "3️⃣ اختر إنشاء حساب ثم لنفسي.\n\n"
            "4️⃣ أكتب الأسم الموجود بالأسفل واي تاريخ ميلاد.\n\n"
            "5️⃣ عند خطوة عنوان الجيميل استخدم هذا اليوزر\n\n"
            "⚠️ كتابة باسورد مختلف قد يعرض حسابك للحظر ومنع سحب أرباحك.\n\n"
            "👇 بعد الانتهاء اختر واحدًا من الأزرار بالأسفل:"
        ),
        'TASKS_AUTO_STEPS': "",
        
        'WALLET_TITLE': "💰 المحفظة",
        'WALLET_WITHDRAW_REQ': "💸 طلب سحب رصيد",
        'WALLET_MIN_LIMIT': "الحد الأدنى للسحب هو $%.2f. استمر في العمل!",
        'WALLET_METHOD_LBL': "طريقة الدفع",
        'WALLET_METHOD_PH': "اختر الطريقة...",
        'WALLET_AMOUNT_LBL': "المبلغ (USD)",
        'WALLET_AVAIL': "المتاح: $%.2f",
        'WALLET_ADDR_LBL': 'عنوان المحفظة',
        'WALLET_ADDR_PH': 'أدخل العنوان هنا...',
        'WALLET_LBL_VODA': 'رقم فودافون كاش',
        'WALLET_LBL_BINANCE': 'معرف باينانس (Pay ID / UID)',
        'WALLET_LBL_USDT': 'عنوان محفظة USDT (BEP20)',
        'WALLET_LBL_TRX': 'عنوان محفظة TRX (TRC20)',
        'WALLET_SUBMIT_BTN': 'إرسال طلب السحب',
        'WALLET_HISTORY': "📜 سجل السحب",
        'WALLET_EMPTY': "لا توجد عمليات سحب حتى الآن.",
        'CONFIRM_TITLE': "تأكيد طلب السحب",
        'CONFIRM_METHOD': "طريقة السحب:",
        'CONFIRM_AMOUNT': "المبلغ:",
        'CONFIRM_WALLET': "العنوان / الرقم:",
        'CONFIRM_BTN': "تأكيد السحب",
        'EDIT_BTN': "تعديل",
        
        'REF_TITLE': "👥 الإحالات",
        'REF_LINK_TITLE': "🔗 رابط الإحالة الخاص بك",
        'REF_COPY_BTN': "نسخ",
        'REF_INVITED': "مدعو",
        'REF_ACTIVE': "نشط",
        'REF_PROFIT': "الأرباح",
        'REF_LIST_TITLE': "👥 المستخدمين المدعوين",
        'REF_EMPTY': "لا يوجد إحالات حتى الآن.<br>شارك رابطك وابدأ بالربح!",
        'REF_BONUS_TEXT': "اربح <b>$%.2f</b> عن كل مهمة مقبولة من إحالاتك",
        'REF_STATUS_ACTIVE': "✅ نشط",
        'REF_STATUS_WAITING': "⏳ في الانتظار",
        
        'FLASH_INVALID_GMAIL': "⚠️ يرجى إدخال عنوان Gmail صحيح.",
        'FLASH_ALREADY_SUBMITTED': "❌ تم إرسال هذا العنوان من قبل! يرجى إرسال عنوان مختلف.",
        'FLASH_TASK_SUCCESS': "✅ تم تقديم المهمة بنجاح!",
        'STATUS_PENDING': "قيد الانتظار",
        'STATUS_APPROVED': "مقبول",
        'STATUS_REJECTED': "مرفوض",
        'STATUS_COMPLETED': "مكتمل",
        'FLASH_INVALID_AMOUNT': "⚠️ مبلغ غير صحيح.",
        'FLASH_METHOD_MIN': "⚠️ الحد الأدنى للسحب لهذه الطريقة هو ${:.2f}.",
        'FLASH_INSUFFICIENT': "⚠️ رصيد غير كافٍ.",
        'FLASH_NO_WALLET': "⚠️ يرجى إدخال عنوان المحفظة.",
        'FLASH_BALANCE_BELOW_MIN': "❌ رصيدك أقل من الحد الأدنى للسحب لهذه الطريقة (${:.2f})",
        'FLASH_WITHDRAW_SUCCESS': "✅ تم إرسال طلب السحب بنجاح!",
        'REF_TASKS_LABEL': "مهمة",
        'HISTORY_STATUS': "الحالة:",
        'HISTORY_METHOD': "الطريقة:",
        'HISTORY_GMAIL': "الجيميل:",
        'HISTORY_PRICE': "المبلغ:",
        'HISTORY_ADDR': "العنوان:",
        'HISTORY_DATE': "التاريخ:",
        'REF_USERNAME': "اسم المستخدم:",
        'REF_USER_ID': "آيدي المستخدم:",
        'REF_DATE': "تاريخ الانضمام:",
        'REF_TASKS': "التاسكات:",
        'REF_PROFIT_EARNED': "الأرباح",
        'DASH_PAY_ID': "رقم الدفع:",
        'PAGE_LABEL': "صفحة",
        'OF_LABEL': "من",
    },
    'en': {
        'NAV_HOME': "Home",
        'NAV_TASKS': "Tasks",
        'NAV_WALLET': "Wallet",
        'NAV_REFERRALS': "Referrals",
        'BTN_PREV_PAGE_INLINE': "Back",

        'BANNED_TITLE': "✋ You are Banned",
        'BANNED_MSG': "❌ <b>Sorry, you have been banned from using the system.</b>\nYour access to the dashboard has been restricted due to a violation of the rules.",
        
        'HOME_WELCOME': "Welcome back 👋",
        'HOME_GREETING': "We are glad to see you again",
        'HOME_BALANCE': "Available Balance",
        'HOME_CURRENT_BALANCE': "Current Balance",
        'HOME_TOTAL_WITHDRAWN': "Total Withdrawn",
        'HOME_PENDING': "⏳ Pending: $%.2f",
        'HOME_USD': "USD",
        'HOME_QUICK_ACTIONS': "Quick Actions",
        'HOME_NEW_TASK': "New Task",
        'HOME_EARN_REWARDS': "Start earning rewards",
        'HOME_WITHDRAW': "Withdraw",
        'HOME_MANAGE_FUNDS': "Manage your funds",
        'HOME_INVITE': "Invite",
        'HOME_INVITE_EARN': "Invite and earn",
        'HOME_SECURE': "Secure",
        'HOME_ENCRYPTED': "End-to-end encrypted",
        'HOME_STATS': "📊 Your Stats",
        'HOME_APPROVED': "Approved",
        'HOME_REJECTED': "Rejected",
        'HOME_REQ_PENDING': "Pending",
        'HOME_RECENT_TASKS': "📋 Recent Tasks",
        'HOME_VIEW_ALL': "View all ←",
        
        'TASKS_TITLE': "📱 Tasks",
        'TASKS_CREATE_GMAIL': "Create Gmail Account",
        'TASKS_EARN': "Earn <b>$%.2f</b> per account",
        'TASKS_SUBTITLE_EARN': "Start earning now by creating a new Gmail account with just one click. 🚀",
        'TASKS_START': "Start New Task",
        'TASKS_PAUSED': "🚧 Task creation is temporarily paused.",
        'TASKS_HISTORY': "📋 Submission History",
        'TASKS_EMPTY': "No tasks yet.<br>Start earning by creating Gmail accounts!",
        'TASKS_REJECTED_HINT': "Review the task instructions and try again.",
        
        'TASK_START_TITLE': "📱 New Gmail Task",
        'TASK_START_INSTRUCTIONS': "📋 Instructions",
        'TASK_START_PWD': "🔑 <b>Unified Password:</b> <code class='copyable'>{}</code>",
        'TASK_START_RULE1': "📱 Create from your phone only",
        'TASK_START_RULE2': "👤 Use any foreign name",
        'TASK_START_RULE3': "📧 Use unified password above",
        'TASK_START_RULE4': "⚠️ Reward after admin approval",
        'TASK_START_RULE5': "🕐 Take your time — no limit",
        'TASK_START_STEPS': "📝 Steps",
        'TASK_START_STEP1': "1️⃣ Create Gmail with password above",
        'TASK_START_STEP2': "2️⃣ Enter address below",
        'TASK_START_STEP_3': '3️⃣ Once finished, just send the email here.',
        'TASK_START_SUBMIT_LBL': "📧 Gmail Address",
        'TASK_START_SUBMIT_PH': "Enter your Gmail here...",
        'TASK_START_SUBMIT_BTN': "Submit Task",
        'TASK_START_BACK': "Back to Tasks",
        'TASKS_MANUAL_MSG': (
            "📱 <b>Gmail Creation Task ⛳️</b>\n\n"
            "📋 <b>Instructions 🥊</b>\n\n"
            "🔑 Unified Password ☜ <code>{password}</code>\n\n"
            "📱 Account must be created from phone only\n\n"
            "👤 Use any foreign name followed by 3 or 4 digits 💁‍♂️\n\n"
            "📧 Use the unified password mentioned above 🕺\n\n"
            "⚠️ You will get the reward after admin approval 💸\n\n"
            "💡 After creating the account, enter the email below 📲\n\n"
            "🕐 Take your time - no time limit for this task ⏳"
        ),
        
        'TASK_TAB_MANUAL': "Manual Create",
        'TASK_TAB_AUTO': "Auto Create",
        'BTN_METHOD_MANUAL': "Manual - {manual_price_text}",
        'BTN_METHOD_AUTO': "Auto - {auto_price_text}",
        'TASK_AUTO_INFO': "",
        'TASK_AUTO_FNAME': "First Name:",
        'TASK_AUTO_LNAME': "Last Name:",
        'TASK_AUTO_EMAIL': "Username:",
        'TASK_AUTO_PWD': "Password:",
        'TASK_AUTO_BTN': "Done",
        'TASK_AUTO_REGEN': "Change Data",
        'TASK_AUTO_CANCEL': "❌ Cancel Registration",
        'TASK_AUTO_WARNING': "⚠️ Writing a different password may expose your account to a ban and prevent withdrawing your profits.",
        'TASK_AUTO_FOOTER': "👇 After finishing, choose one of the buttons below:",
        'TASKS_AUTO_INSTRUCTIONS': (
            "📱 <b>New Gmail Task</b>\n\n"
            "✨ Follow the steps calmly and in order:\n\n"
            "1️⃣ Go to Settings then Users & Accounts.\n\n"
            "2️⃣ Click Add Account then choose Google.\n\n"
            "3️⃣ Choose Create Account then For Myself.\n\n"
            "4️⃣ Write the name below and any birthday.\n\n"
            "5️⃣ At the Gmail address step use this username\n\n"
            "⚠️ Writing a different password may expose your account to a ban and prevent withdrawing your profits.\n\n"
            "👇 After finishing, choose one of the buttons below:"
        ),
        'TASKS_AUTO_STEPS': "",
        
        'WALLET_TITLE': "💰 Wallet",
        'WALLET_WITHDRAW_REQ': "💸 Request Withdrawal",
        'WALLET_MIN_LIMIT': "Min withdrawal is $%.2f. Keep earning!",
        'WALLET_METHOD_LBL': "Payment Method",
        'WALLET_METHOD_PH': "Select method...",
        'WALLET_AMOUNT_LBL': "Amount (USD)",
        'WALLET_AVAIL': "Available: $%.2f",
        'WALLET_ADDR_LBL': 'Wallet Address',
        'WALLET_ADDR_PH': 'Enter address here...',
        'WALLET_LBL_VODA': 'Vodafone Cash Number',
        'WALLET_LBL_BINANCE': 'Binance Pay ID or UID',
        'WALLET_LBL_USDT': 'USDT (BEP20) Wallet Address',
        'WALLET_LBL_TRX': 'TRX (TRC20) Wallet Address',
        'WALLET_SUBMIT_BTN': 'Submit Withdrawal',
        'WALLET_HISTORY': "📜 Withdrawal History",
        'WALLET_EMPTY': "No withdrawals yet.",
        'CONFIRM_TITLE': "Confirm Withdrawal",
        'CONFIRM_METHOD': "Method:",
        'CONFIRM_AMOUNT': "Amount:",
        'CONFIRM_WALLET': "Address / Number:",
        'CONFIRM_BTN': "Confirm Withdrawal",
        'EDIT_BTN': "Edit",
        
        'REF_TITLE': "👥 Referrals",
        'REF_LINK_TITLE': "🔗 Your Referral Link",
        'REF_COPY_BTN': "Copy",
        'REF_INVITED': "Invited",
        'REF_ACTIVE': "Active",
        'REF_PROFIT': "Profit",
        'REF_LIST_TITLE': "👥 Invited Users",
        'REF_EMPTY': "No referrals yet.<br>Share your link and earn!",
        'REF_BONUS_TEXT': "Earn <b>$%.2f</b> per approved task from referrals",
        'REF_STATUS_ACTIVE': "✅ Active",
        'REF_STATUS_WAITING': "⏳ Waiting",
        
        'FLASH_INVALID_GMAIL': "⚠️ Please enter a valid Gmail address.",
        'FLASH_ALREADY_SUBMITTED': "❌ This Gmail has already been submitted! Please send a different address.",
        'FLASH_TASK_SUCCESS': "✅ Task submitted successfully!",
        'STATUS_PENDING': "Pending",
        'STATUS_APPROVED': "Approved",
        'STATUS_REJECTED': "Rejected",
        'STATUS_COMPLETED': "Completed",
        'FLASH_INVALID_AMOUNT': "⚠️ Invalid amount.",
        'FLASH_METHOD_MIN': "⚠️ Minimum for this method is ${:.2f}.",
        'FLASH_INSUFFICIENT': "⚠️ Insufficient balance.",
        'FLASH_NO_WALLET': "⚠️ Please enter a wallet address.",
        'FLASH_BALANCE_BELOW_MIN': "❌ Your balance is below the minimum for this method (${:.2f})",
        'FLASH_WITHDRAW_SUCCESS': "✅ Withdrawal request submitted!",
        'REF_TASKS_LABEL': "tasks",
        'HISTORY_STATUS': "Status:",
        'HISTORY_METHOD': "Method:",
        'HISTORY_GMAIL': "Gmail:",
        'HISTORY_PRICE': "Price:",
        'HISTORY_ADDR': "Address:",
        'HISTORY_DATE': "Date:",
        'REF_USERNAME': "Username:",
        'REF_USER_ID': "User ID:",
        'REF_DATE': "Join Date:",
        'REF_TASKS': "Tasks:",
        'REF_PROFIT_EARNED': "Earning:",
        'DASH_PAY_ID': "Pay ID:",
        'PAGE_LABEL': "Page",
        'OF_LABEL': "of",
    }
}

DASHBOARD_STRINGS = {
    'ar': {
        'NAV_HOME': "الرئيسية",
        'NAV_TASKS': "المهام",
        'DASH_UPDATE_BTN': 'تعديل',
        'LBL_UNIFIED_PWD': 'كلمة المرور الموحدة (لليدوي)',
        'LBL_CUSTOM_PRICES': 'أسعار مخصصة',
        'DASH_INDEX_TITLE': "نظرة عامة",
        'NAV_PAY': "الدفع",
        'NAV_USERS': "المستخدمين",
        'NAV_MSG': "البث",
        'NAV_SET': "الإعدادات",
        
        'DASH_INDEX_TITLE': "نظرة عامة",
        'DASH_USERS_SECTION': "المستخدمين",
        'DASH_TOTAL_USERS': "إجمالي المستخدمين",
        'DASH_BANNED_USERS': "محظورين",
        'DASH_TASKS_SECTION': "المهام",
        'DASH_TOTAL_TASKS': "إجمالي المهام",
        'DASH_APPROVED': "مقبول",
        'DASH_PENDING': "قيد الانتظار",
        'DASH_REJECTED': "مرفوض",
        'DASH_WITHDRAWALS_SECTION': "عمليات السحب",
        'DASH_TOTAL_REQS': "إجمالي الطلبات",
        'DASH_COMPLETED': "مكتمل",
        
        'DASH_TASKS_PAGE_TITLE': "تقديمات المهام",
        'DASH_FILTER_ALL': "الكل",
        'DASH_FILTER_PENDING': "قيد الانتظار",
        'DASH_FILTER_PAID': "مقبول",
        'DASH_FILTER_REJECTED': "مرفوض",
        'DASH_AGE_1D': "يوم واحد",
        'DASH_AGE_2D': "يومين",
        'DASH_AGE_3D': "3 أيام",
        'DASH_SEARCH_USER_PH': "ID / Gmail / User...",
        'DASH_PAY_SEARCH_PH': "ID / Wallet / User...",
        'DASH_SEARCH_DATE_PH': "التاريخ...",
        'DASH_FIND_BTN': "بحث",
        'DASH_RESET_BTN': "إعادة ضبط",
        'DASH_QUEUE_TITLE': "قائمة التقديمات",
        'DASH_RESULTS': "نتائج",
        'DASH_LBL_TASK_ID': "رقم المهمة:",
        'DASH_LBL_GMAIL': "حساب جيميل:",
        'DASH_LBL_PASSWORD': "كلمة المرور:",
        'DASH_LBL_PRICE': "السعر:",
        'DASH_LBL_DATE': "التاريخ:",
        'DASH_LBL_USER_ID': "معرف المستخدم:",
        'DASH_NO_TASKS': "لا توجد تقديمات.",
        'DASH_APPROVE_TASK': "قبول المهمة",
        'DASH_REJECT_TASK': "رفض المهمة",
        'NAV_CUSTOM_PRICES': "مستخدمين VIP",
        'NAV_LEADERBOARD': "لوحة المتصدرين",
        'DASH_CP_PAGE_TITLE': "مستخدمين VIP",
        'DASH_CP_LABEL': "السعر المخصص:",
        'DASH_CP_RESET_BTN': "إزالة التخصيص",
        'DASH_CP_NO_USERS': "لا يوجد مستخدمين بأسعار مخصصة حالياً.",
        'DASH_LB_TITLE': "لوحة المتصدرين",
        'DASH_LB_APPROVED': "الأكثر قبولاً",
        'DASH_LB_REJECTED': "الأكثر رفضاً",
        'DASH_LB_WITHDRAWN': "الأكثر سحباً",
        'DASH_LB_COUNT': "العدد",
        'DASH_LB_TOTAL': "الإجمالي",
        'DASH_LB_EMPTY': "لا توجد بيانات كافية.",
        'DASH_CONFIRM_REJECT': "تأكيد الرفض",
        'DASH_REJECT_MSG': "هل أنت متأكد من رفض هذا التاسك؟ سيتم إخطار المستخدم.",
        'DASH_CANCEL': "إلغاء",
        'DASH_MODAL_REJECT_BTN': "رفض",
        
        'DASH_W_PAGE_TITLE': "عمليات السحب",
        'DASH_W_REQS': "طلبات السحب",
        'DASH_TOTAL_PAID_AMOUNT': "إجمالي المبالغ المدفوعة",
        'DASH_REJECTED_TASKS_VALUE': "قيمة المهام المرفوضة",
        'DASH_FINANCIALS_SECTION': "الماليات",
        'DASH_NO_WITHDRAWALS': "لا توجد طلبات سحب.",
        'DASH_MARK_PAID': "تحديد كمدفوع",
        'DASH_PAY_ID': "رقم الدفع:",
        'HISTORY_STATUS': "الحالة:",
        'HISTORY_METHOD': "طريقة السحب:",
        'HISTORY_PRICE': "المبلغ:",
        'HISTORY_ADDR': "العنوان:",
        'HISTORY_DATE': "التاريخ:",
        'DASH_REASON': "السبب",
        
        'DASH_U_PAGE_TITLE': "إدارة المستخدمين",
        'DASH_U_SEARCH_PH': "بحث عن مستخدمين...",
        'DASH_U_EDIT': "تعديل المستخدم",
        'DASH_U_ADJUST_BAL': "تعديل الرصيد",
        'DASH_U_BAN': "حظر الحساب",
        'DASH_U_UNBAN': "إلغاء الحظر",
        'DASH_U_BALANCE': "الرصيد",
        'DASH_U_HOLD': "معلق",
        'DASH_U_TASKS': "مهام",
        'DASH_U_STATUS_ACTIVE': "نشط",
        'DASH_U_STATUS_BANNED': "محظور",
        'DASH_U_TOTAL_WITHDRAWN': "إجمالي المسحوبات",
        
        'DASH_BS_PAGE_TITLE': "إرسال رسائل",
        'DASH_BS_ALL': "إرسال للجميع (برودكاست)",
        'DASH_BS_USER': "إرسال لمستخدم محدد",
        'DASH_BS_CONTENT': "محتوى الرسالة (يدعم HTML)",
        'DASH_BS_SEND_BTN': "إرسال الآن",
        'DASH_BS_PH': "اكتب رسالتك هنا...",
        'DASH_BS_USER_ID': "معرف المستخدم (ID)",

        'SETTINGS_TITLE': "الإعدادات",
        'SETTINGS_CAT_GENERAL': "الأسعار والعمولات",
        'SETTINGS_CAT_CHANNELS': "القنوات والاشتراكات",
        'SETTINGS_CAT_LIMITS': "حدود السحب",
        'SETTINGS_CAT_CONTROL': "التحكم واللغة",
        'SETTINGS_CAT_RESET': "إعادة الضبط",
        'SETTINGS_LOGOUT': "تسجيل الخروج",
        
        'SETTINGS_CONFIG': "إعدادات البوت",
        'SETTINGS_BOT_NAME': "اسم البوت",
        'SETTINGS_GMAIL_MANUAL_PRICE': "سعر الجيميل اليدوي ($)",
        'SETTINGS_GMAIL_AUTO_PRICE': "سعر الجيميل التلقائي ($)",
        'LBL_MANUAL_PWD': "كلمة المرور الموحدة (يدوي)",
        'LBL_AUTO_PWD': "كلمة المرور الموحدة (تلقائي)",
        'LBL_CUSTOM_MANUAL': "يدوي",
        'LBL_CUSTOM_AUTO': "تلقائي",
        'LBL_BACK': "رجوع",
        'SETTINGS_REF_BONUS': "مكافأة الإحالة ($)",
        'LBL_TASK_TIMEOUT': "مدة المهمة (بالدقائق)",
        'SETTINGS_MIN_WITHDRAWALS': "حدود السحب الأدنى لكل طريقة:",
        'SETTINGS_VODAFONE': "فودافون كاش ($)",
        'SETTINGS_BINANCE': "بينانس ($)",
        'SETTINGS_USDT': "USDT (BEP20) ($)",
        'SETTINGS_TRX': "TRX (TRC20) ($)",
        'SETTINGS_BUYING_STATUS': "حالة شراء المهام",
        'SETTINGS_ACTIVE': "🟢 نشط",
        'SETTINGS_PAUSED': "🔴 متوقف",
        'SETTINGS_UPDATE_BTN': "تحديث الإعدادات",
        'SETTINGS_LANG': "لغة لوحة التحكم",
        'SETTINGS_REQ_CHANNELS': "قنوات الاشتراك الإجباري",
        'SETTINGS_REQ_CHANNELS_HELP': "افصل بين القنوات بفاصلة إذا كان هناك أكثر من قناة (مثال: @channel1,@channel2).",
        'SETTINGS_NOTIFY_CHANNELS': "قنوات الإشعارات",
        'SETTINGS_EMAILS_CHANNEL': "قناة طلبات الجيميل (ID)",
        'SETTINGS_WITHDRAWALS_CHANNEL': "قناة طلبات السحب (ID)",
        'ALERT_SETTINGS_SAVED': "تم تحديث الإعدادات بنجاح! التغييرات نشطة الآن للبوت.",
        'ALERT_LOGIN_SUCCESS': "تم تسجيل الدخول بنجاح.",
        'LBL_RESET_SETTINGS': "إعادة التعيين ♻️",
        'LBL_GLOBAL_RESET': "إعادة تعيين شاملة (تصفير الكل)",
        'LBL_GLOBAL_RESET_DESC': "تصفير جميع الإحصائيات والأرصدة لكل المستخدمين، ولكن يتم الاحتفاظ بحساباتهم مسجلة.",
        'LBL_USER_RESET': "إعادة تعيين بيانات مستخدم محدد",
        'LBL_USER_RESET_DESC': "تصفير الأرصدة وإلغاء إحصائيات مستخدم معين برقم الآيدي الخاص به بدون حذفه.",
        'LBL_USER_ID': "رقم آيدي المستخدم (User ID)",
        'BTN_RESET_GLOBAL': "بدء إعادة التعيين الشاملة ⚠️",
        'BTN_RESET_USER': "تصفير بيانات المستخدم 👤",
        'MSG_RESET_CONFIRM': "هل أنت متأكد؟ لا يمكن التراجع عن هذه العملية.",
        'ALERT_RESET_SUCCESS': "تمت عملية إعادة التعيين بنجاح.",
        'ALERT_RESET_ERROR': "حدث خطأ أثناء المحاولة. تأكد من صحة الآيدي أو البيانات.",
        'LBL_DELETE_ALL_USERS': "حذف جميع المستخدمين",
        'LBL_DELETE_ALL_DESC': "حذف كل بيانات المستخدمين، وحذف حساباتهم، وتصفير المهام بالكامل، عملية لا رجعة فيها.",
        'BTN_DELETE_ALL_USERS': "حذف الكل نهائياً ☠️",
        'LBL_DELETE_SPECIFIC_USER': "حذف مستخدم محدد بكل بياناته",
        'LBL_DELETE_SPECIFIC_DESC': "حذف مستخدم معين وحسابه بالكامل من قاعدة البيانات بناءً على الآيدي الخاص به.",
        'BTN_DELETE_SPECIFIC_USER': "حذف المستخدم نهائياً 🗑️",
        'ALERT_DELETE_SUCCESS': "تم الحذف بنجاح.",
        'ALERT_DELETE_ERROR': "حدث خطأ أثناء الحذف. تأكد من صحة الآيدي.",
        
        'PAGE_LABEL': "صفحة",
        'OF_LABEL': "من",
        'TITLE_APP': "جيميل فارمر",
    },
    'en': {
        'NAV_HOME': "Home",
        'NAV_TASKS': "Tasks",
        'DASH_UPDATE_BTN': 'Update',
        'LBL_UNIFIED_PWD': 'Unified Manual Password',
        'LBL_CUSTOM_PRICES': 'Custom Prices',
        'NAV_PAY': "Pay",
        'NAV_USERS': "Users",
        'NAV_MSG': "Broadcast",
        'NAV_SET': "Settings",
        
        'DASH_INDEX_TITLE': "Overview",
        'DASH_USERS_SECTION': "Users",
        'DASH_TOTAL_USERS': "Total Users",
        'DASH_BANNED_USERS': "Banned",
        'DASH_TASKS_SECTION': "Tasks",
        'DASH_TOTAL_TASKS': "Total Tasks",
        'DASH_APPROVED': "Approved",
        'DASH_PENDING': "Pending",
        'DASH_REJECTED': "Rejected",
        'DASH_WITHDRAWALS_SECTION': "Withdrawals",
        'DASH_TOTAL_REQS': "Total Requests",
        'DASH_COMPLETED': "Completed",
        
        'DASH_TASKS_PAGE_TITLE': "Task Submissions",
        'DASH_FILTER_ALL': "All",
        'DASH_FILTER_PENDING': "Pending",
        'DASH_FILTER_PAID': "Approved",
        'DASH_FILTER_REJECTED': "Rejected",
        'DASH_AGE_1D': "1 Day",
        'DASH_AGE_2D': "2 Days",
        'DASH_AGE_3D': "3 Days",
        'DASH_SEARCH_USER_PH': "ID / Gmail / User...",
        'DASH_PAY_SEARCH_PH': "ID / Wallet / User...",
        'DASH_SEARCH_DATE_PH': "Date...",
        'DASH_FIND_BTN': "Find",
        'DASH_RESET_BTN': "Reset",
        'DASH_QUEUE_TITLE': "Submission Queue",
        'DASH_RESULTS': "results",
        'DASH_LBL_TASK_ID': "Task ID:",
        'DASH_LBL_GMAIL': "Gmail:",
        'DASH_LBL_PASSWORD': "Password:",
        'DASH_LBL_PRICE': "Price:",
        'DASH_LBL_DATE': "Date:",
        'DASH_PAY_ID': "Pay ID:",
        'HISTORY_STATUS': "Status:",
        'HISTORY_METHOD': "Method:",
        'HISTORY_PRICE': "Price:",
        'HISTORY_ADDR': "Address:",
        'HISTORY_DATE': "Date:",
        'DASH_LBL_USER_ID': "User ID:",
        'DASH_NO_TASKS': "No submissions found.",
        'DASH_APPROVE_TASK': "Approve Submission",
        'DASH_REJECT_TASK': "Reject Submission",
        'NAV_CUSTOM_PRICES': "VIP Users",
        'NAV_LEADERBOARD': "Leaderboard",
        'DASH_CP_PAGE_TITLE': "VIP Users",
        'DASH_CP_LABEL': "Custom Price:",
        'DASH_CP_RESET_BTN': "Reset Default",
        'DASH_CP_NO_USERS': "No users with custom prices found.",
        'DASH_LB_TITLE': "Leaderboard",
        'DASH_LB_APPROVED': "Top Approved",
        'DASH_LB_REJECTED': "Top Rejected",
        'DASH_LB_WITHDRAWN': "Top Withdrawn",
        'DASH_LB_COUNT': "Count",
        'DASH_LB_TOTAL': "Total",
        'DASH_LB_EMPTY': "No data available.",
        'DASH_CONFIRM_REJECT': "Confirm Rejection",
        'DASH_REJECT_MSG': "Are you sure you want to reject this task? User will be notified.",
        'DASH_CANCEL': "Cancel",
        'DASH_MODAL_REJECT_BTN': "Reject",
        
        'DASH_W_PAGE_TITLE': "Withdrawals",
        'DASH_W_REQS': "Withdrawal Requests",
        'DASH_TOTAL_PAID_AMOUNT': "Total Amount Paid",
        'DASH_REJECTED_TASKS_VALUE': "Rejected Tasks Value",
        'DASH_FINANCIALS_SECTION': "Financials",
        'DASH_NO_WITHDRAWALS': "No requests found.",
        'DASH_MARK_PAID': "Mark Paid",
        'DASH_REASON': "Reason",
        
        'DASH_U_PAGE_TITLE': "User Management",
        'DASH_U_SEARCH_PH': "Search users...",
        'DASH_U_EDIT': "Edit User",
        'DASH_U_ADJUST_BAL': "Adjust Balance",
        'DASH_U_BAN': "Ban Account",
        'DASH_U_UNBAN': "Unban User",
        'DASH_U_BALANCE': "Balance",
        'DASH_U_HOLD': "Hold",
        'DASH_U_TASKS': "Tasks",
        'DASH_U_STATUS_ACTIVE': "Active",
        'DASH_U_STATUS_BANNED': "Banned",
        'DASH_U_TOTAL_WITHDRAWN': "Total Withdrawn",
        
        'DASH_BS_PAGE_TITLE': "Broadcast",
        'DASH_BS_ALL': "Send to All",
        'DASH_BS_USER': "Send to User",
        'DASH_BS_CONTENT': "Message Content (HTML)",
        'DASH_BS_SEND_BTN': "Send Message",
        'DASH_BS_PH': "Type your message here...",
        'DASH_BS_USER_ID': "User ID",

        'SETTINGS_TITLE': "Settings",
        'SETTINGS_CAT_GENERAL': "Prices & Commissions",
        'SETTINGS_CAT_CHANNELS': "Channels & Subscriptions",
        'SETTINGS_CAT_LIMITS': "Withdrawal Limits",
        'SETTINGS_CAT_CONTROL': "Control & Language",
        'SETTINGS_CAT_RESET': "Reset Options",
        'SETTINGS_LOGOUT': "Logout",

        'SETTINGS_CONFIG': "Bot Configuration",
        'SETTINGS_BOT_NAME': "Bot Name",
        'SETTINGS_GMAIL_MANUAL_PRICE': "Manual Gmail Price ($)",
        'SETTINGS_GMAIL_AUTO_PRICE': "Auto Gmail Price ($)",
        'LBL_MANUAL_PWD': "Manual Unified Password",
        'LBL_AUTO_PWD': "Auto Unified Password",
        'LBL_CUSTOM_MANUAL': "Manual",
        'LBL_CUSTOM_AUTO': "Auto",
        'LBL_BACK': "Back",
        'SETTINGS_REF_BONUS': "Ref Bonus ($)",
        'LBL_TASK_TIMEOUT': "Task Timeout (Minutes)",
        'SETTINGS_MIN_WITHDRAWALS': "Minimum withdrawal limits:",
        'SETTINGS_VODAFONE': "Vodafone ($)",
        'SETTINGS_BINANCE': "Binance ($)",
        'SETTINGS_USDT': "USDT (BEP20) ($)",
        'SETTINGS_TRX': "TRX (TRC20) ($)",
        'SETTINGS_BUYING_STATUS': "Buying Tasks Status",
        'SETTINGS_ACTIVE': "🟢 Active",
        'SETTINGS_PAUSED': "🔴 Paused",
        'SETTINGS_UPDATE_BTN': "Update Settings",
        'SETTINGS_LANG': "Dashboard Language",
        'SETTINGS_REQ_CHANNELS': "Mandatory Subscription Channels",
        'SETTINGS_REQ_CHANNELS_HELP': "Separate multiple channels with a comma (e.g., @channel1,@channel2).",
        'SETTINGS_NOTIFY_CHANNELS': "Notification Channels",
        'SETTINGS_EMAILS_CHANNEL': "Emails Channel ID",
        'SETTINGS_WITHDRAWALS_CHANNEL': "Withdrawals Channel ID",
        'ALERT_SETTINGS_SAVED': "Settings updated successfully! Changes are now active for the bot.",
        'ALERT_LOGIN_SUCCESS': "Successfully logged in.",
        'LBL_RESET_SETTINGS': "Data Reset ♻️",
        'LBL_GLOBAL_RESET': "Reset all user data",
        'LBL_GLOBAL_RESET_DESC': "Cleans all tasks and withdrawal histories for everyone, but keeps their accounts registered.",
        'LBL_USER_RESET': "Specific User Reset",
        'LBL_USER_RESET_DESC': "Resets a single user's balance and task history to zero without deleting their account.",
        'LBL_USER_ID': "User ID",
        'BTN_RESET_GLOBAL': "Start Global Reset ⚠️",
        'BTN_RESET_USER': "Reset User Data 👤",
        'MSG_RESET_CONFIRM': "Are you sure? This action is permanent.",
        'ALERT_RESET_SUCCESS': "Reset performed successfully.",
        'ALERT_RESET_ERROR': "An error occurred. Please check the User ID or data.",
        'LBL_DELETE_ALL_USERS': "Delete All Users",
        'LBL_DELETE_ALL_DESC': "Performs a complete wipe of all user records, tasks, and accounts. Fully irreversible.",
        'BTN_DELETE_ALL_USERS': "Delete All ☠️",
        'LBL_DELETE_SPECIFIC_USER': "Delete Specific User",
        'LBL_DELETE_SPECIFIC_DESC': "Deletes a specific user completely from the database, dropping all their data permanently.",
        'BTN_DELETE_SPECIFIC_USER': "Delete User 🗑️",
        'ALERT_DELETE_SUCCESS': "Deletion completed successfully.",
        'ALERT_DELETE_ERROR': "An error occurred during deletion. Please check the User ID.",
        
        'PAGE_LABEL': "Page",
        'OF_LABEL': "of",
    }
}



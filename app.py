from flask import Flask, request, jsonify
import json
import os

# استيراد منطق الوكيل من الملف الأصلي
from ai_agent_logic import GLOSSARY, PHASES, AGENT_SCRIPTS

app = Flask(__name__)

# ==============================================================================
# دالة لمعالجة منطق الوكيل (يمكن تطويرها لاحقاً)
# ==============================================================================
def process_agent_logic(user_message):
    """
    هذه دالة وهمية لمعالجة رسالة المستخدم وتحديد الرد المناسب.
    في التطبيق الفعلي، سيتم استخدام ChatGPT API هنا.
    """
    # تحويل رسالة المستخدم إلى حروف صغيرة لتسهيل المقارنة
    msg = user_message.lower()

    # محاكاة بسيطة لمنطق الردود بناءً على المراحل
    if "مهتمة" in msg or "نعم" in msg:
        # الرد على الاهتمام - المرحلة 2
        response = {
            "phase": 2,
            "message": AGENT_SCRIPTS["PHASE_2_INTRO"],
            "next_step": "الانتظار لتنزيل التطبيق أو الأسئلة"
        }
    elif "رقمي" in msg or "واتساب" in msg:
        # الرد على طلب الرقم - المرحلة 3
        response = {
            "phase": 3,
            "message": AGENT_SCRIPTS["PHASE_3_WHATSAPP_WELCOME"],
            "next_step": "إرسال فيديوهات التوثيق"
        }
    elif "سلام" in msg or "مرحبا" in msg:
        # رسالة ترحيب أولية - المرحلة 1
        response = {
            "phase": 1,
            "message": AGENT_SCRIPTS["PHASE_1_DM"],
            "next_step": "الانتظار لرد الفتاة بـ 'Trigger'"
        }
    else:
        # رد افتراضي (يمكن استبداله بـ ChatGPT API)
        response = {
            "phase": 0,
            "message": "مرحباً! أنا وكيل الذكاء الاصطناعي. حالياً، أنا أعمل على الردود التلقائية. إذا كنتِ مهتمة بالعمل، اكتبي 'مهتمة' لأبدأ معك الخطوات. (هذا رد آلي مؤقت)",
            "next_step": "الانتظار لـ 'Trigger'"
        }

    return response

# ==============================================================================
# نقطة النهاية (Endpoint) الرئيسية التي ستستقبل طلبات ManyChat
# ==============================================================================
@app.route('/webhook', methods=['POST'])
def webhook():
    """
    نقطة النهاية التي يستدعيها ManyChat لإرسال رسائل المستخدم.
    """
    try:
        # ManyChat يرسل البيانات كـ JSON
        data = request.get_json()
        
        # استخراج رسالة المستخدم (قد تختلف طريقة الاستخراج حسب إعدادات ManyChat)
        # نفترض أن ManyChat يرسل رسالة المستخدم في حقل 'message'
        user_message = data.get('message', 'رسالة فارغة')
        
        # استدعاء منطق الوكيل
        agent_response = process_agent_logic(user_message)
        
        # إرجاع الرد إلى ManyChat (يجب أن يكون الرد بصيغة يفهمها ManyChat)
        # هنا نرجع الرد كـ JSON بسيط
        return jsonify({
            "status": "success",
            "reply_text": agent_response["message"],
            "debug_info": agent_response
        })

    except Exception as e:
        # في حال حدوث خطأ، نرجع رسالة خطأ
        return jsonify({
            "status": "error",
            "message": f"حدث خطأ في معالجة الطلب: {str(e)}",
            "debug_info": None
        }), 500

# ==============================================================================
# نقطة نهاية بسيطة للتحقق من أن التطبيق يعمل
# ==============================================================================
@app.route('/', methods=['GET'])
def home():
    """
    صفحة رئيسية بسيطة للتحقق من حالة التطبيق.
    """
    return jsonify({
        "status": "API is running",
        "project": "AI Agent Logic Web API",
        "version": "1.0",
        "note": "This is the Web API for the AI Agent logic. Use /webhook for ManyChat integration."
    })

if __name__ == '__main__':
    # تشغيل التطبيق محلياً (لن يعمل على Railway)
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))

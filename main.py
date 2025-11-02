# -*- coding: utf-8 -*-
import atexit
from openai import OpenAI
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot.config import OPENAI_CONFIG, MODEL_PATH
from chatbot.embeddings.loader import EmbeddingsLoader
from chatbot.interface.gradio_ui import launch_ui
from chatbot.shared_embeddings import set_global_embeddings
from chatbot.monitoring import monitor
from chatbot.chains.chains import ChainSetup


def init_system():
    """Initialize embeddings, model connection, and chains."""
    try:
        monitor.log_system_event("system_startup", {"status": "starting"})

        # === Load embeddings once ===
        embeddings_loader = EmbeddingsLoader()
        embeddings = embeddings_loader.load()
        set_global_embeddings(embeddings)

        monitor.log_system_event("embeddings_loaded", {"status": "success"})
        print("✅ تم تحميل الـ embeddings بنجاح")

        # === Test model connection ===
        client = OpenAI(**OPENAI_CONFIG)
        test_response = client.chat.completions.create(
            model=MODEL_PATH,
            messages=[{"role": "user", "content": "مرحبا"}],
            max_tokens=50
        )

        if test_response.choices[0].message.content:
            monitor.log_system_event("model_connection_test", {"status": "success"})
            print("✅ تم الاتصال بنموذج OpenAI بنجاح")

        # === Initialize LangChain chains (with DB memory) ===
        global chain_setup
        chain_setup = ChainSetup()
        chain_setup.setup_chains()
        print("✅ تم تهيئة سلاسل LangChain والذاكرة بنجاح")

        return True

    except Exception as e:
        error_msg = str(e)
        monitor.log_system_event("system_startup_failed", {"error": error_msg})
        print(f"❌ خطأ أثناء التهيئة: {error_msg}")
        return False


def main():
    """Main entrypoint for local run."""
    if not init_system():
        return

    # === Launch Gradio interface ===
    monitor.log_system_event("gradio_interface_starting", {"status": "starting"})
    print("🚀 تشغيل واجهة Gradio...")

    demo = launch_ui()  # launch_ui now returns the Gradio demo
    demo.launch(server_name="0.0.0.0", server_port=7862, share=False)


# ✅ For uvicorn / FastAPI launch
# This allows `uvicorn main:app --reload` to work
if init_system():
    app = launch_ui()  # expose for uvicorn


# ✅ Automatically save memory before exit
def save_all_contexts():
    """Save chat memory to DB before shutdown."""
    try:
        if 'chain_setup' in globals() and hasattr(chain_setup, 'save_context_to_db'):
            chain_setup.save_context_to_db()
            print("💾 تم حفظ سياق المحادثة قبل الإغلاق.")
    except Exception as e:
        print(f"⚠️ لم يتم حفظ السياق التلقائي: {e}")


atexit.register(save_all_contexts)


if __name__ == "__main__":
    main()

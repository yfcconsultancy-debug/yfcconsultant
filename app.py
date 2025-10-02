from flask import Flask, render_template, request, session, jsonify
from uuid import uuid4

app = Flask(__name__)
app.secret_key = "change_this_secret_key"  # Change in production

# In-memory storage for chat histories
user_chats = {}

# Bot logic with concise replies and shorter buttons
def bot_reply(message):
    """Handles the bot's response logic based on user input."""
    message = message.lower().strip()

    # --- Main Menu & Greetings ---
    if message in ["hi", "hello", "main menu", "⬅ menu"]:
        return {
            "text": "Welcome to FLCS! How can I help you today?",
            "buttons": ["Services", "Packages", "Destinations", "About Us"]
        }

    # --- Branch 1: Explore Services ---
    elif message == "services":
        return {
            "text": "We offer end-to-end support for your study abroad journey. What would you like to know more about?",
            "buttons": ["Admission", "Visa", "Scholarships", "Post-Arrival", "⬅ Menu"]
        }
    elif message == "admission":
        return {
            "text": "We help you choose the right career, select top universities, and draft key documents like SOPs, LORs, and CVs.",
            "buttons": ["Visa", "Scholarships", "⬅ Services"]
        }
    elif message == "visa":
        return {
            "text": "We provide full visa and immigration support, including documentation, mock interviews, and appointment booking. We have a 99% visa success rate!",
            "buttons": ["Admission", "Scholarships", "⬅ Services"]
        }
    elif message == "scholarships":
        return {
            "text": "We assist with scholarship applications, document translation, and legalization. We've helped students secure over ₹20 Crore in scholarships.",
            "buttons": ["Admission", "Visa", "⬅ Services"]
        }
    elif message == "post-arrival":
        return {
            "text": "Our support continues after you land in Italy! We assist with airport pickup, accommodation, residence permits, and opening a bank account.",
            "buttons": ["Admission", "Scholarships", "⬅ Services"]
        }
    elif message == "⬅ services":
         return {
            "text": "What service would you like to know more about?",
            "buttons": ["Admission", "Visa", "Scholarships", "Post-Arrival", "⬅ Menu"]
        }

    # --- Branch 2: Packages & Pricing ---
    elif message in ["packages", "⬅ packages"]:
        return {
            "text": "We offer three packages to fit your needs. Which one would you like to see?",
            "buttons": ["Silver", "Gold", "Platinum", "Compare", "Add-ons", "⬅ Menu"]
        }
    elif message == "silver":
        return {
            "text": "🪙 Silver: Best for self-starters. Includes guidance, document templates, and one mock visa interview.",
            "buttons": ["Gold", "Platinum", "⬅ Packages"]
        }
    elif message == "gold":
        return {
            "text": "🥇 Gold: Our most popular option. We draft your documents, file up to 7 applications with you, and provide 3 mock interviews.",
            "buttons": ["Silver", "Platinum", "⬅ Packages"]
        }
    elif message == "platinum":
        return {
            "text": "💎 Platinum: Our 'done-for-you' solution. We handle everything, from applications to post-arrival support, with many fees included.",
            "buttons": ["Silver", "Gold", "⬅ Packages"]
        }
    elif message == "compare":
        return {
            "text": "Here's a quick comparison:\n\n*🪙 Silver:* Guidance-focused.\n*🥇 Gold:* 'Done-with-you' service.\n*💎 Platinum:* 'Done-for-you' comprehensive solution.",
            "buttons": ["Silver", "Gold", "Platinum", "⬅ Packages"]
        }
    elif message == "add-ons":
        return {
            "text": "We also offer individual services like Italian Translation (₹1500), Mock Interviews (₹5000), and an Accommodation Hunt in Italy (₹15,000).",
            "buttons": ["⬅ Packages"]
        }
    
    # --- Branch 3: Study Destinations ---
    elif message == "destinations":
        return {
            "text": "We specialize in ITALY, but also guide students to GERMANY, USA, UK, CANADA, AUSTRALIA, and more.",
            "buttons": ["About Us", "Packages", "⬅ Menu"]
        }

    # --- Branch 4: Why Choose FLCS? ---
    elif message == "about us":
        return {
            "text": "Why choose FLCS?\n\n*Proven Success:* 99% visa success rate.\n*Expert Team:* Personalized guidance.\n*Transparency:* You get real-time updates.\n*Dual Offices:* Support in both India and Italy.",
            "buttons": ["📞 Contact", "Reviews", "⬅ Menu"]
        }
    elif message == "reviews":
         return {
            "text": "Our students love us! Abhigyan Sharma said we 'genuinely help,' and Ayman Durrani said we 'guided me through the entire process.'",
            "buttons": ["About Us", "📞 Contact", "⬅ Menu"]
        }

    # --- Contact & Fallback ---
    elif message == "📞 contact":
        return {
            "text": "Let's connect!\n\n*Phone:* +91 906 888 7041\n*WhatsApp:* +91 963 903 6869\n*Website:* www.flcs.in",
            "buttons": ["Services", "Packages", "⬅ Menu"]
        }
    elif message in ["bye", "exit"]:
        return {"text": "Goodbye! Have a great day!", "buttons": []}
    else:
        return {
            "text": "Sorry, I didn't understand. Please choose an option below.",
            "buttons": ["Services", "Packages", "About Us"]
        }


# Ensure user has a session ID
@app.before_request
def ensure_session():
    if "user_id" not in session:
        session["user_id"] = str(uuid4())

# Render chat page
@app.route("/")
def index():
    return render_template("index.html")

# Handle messages
@app.route("/send", methods=["POST"])
def send():
    user_id = session.get("user_id")
    if not user_id:
        user_id = str(uuid4())
        session["user_id"] = user_id

    # Ensure user chat history exists
    if user_id not in user_chats:
        user_chats[user_id] = []

    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    user_chats[user_id].append({"from": "user", "text": user_message})
    reply = bot_reply(user_message)
    user_chats[user_id].append({"from": "bot", "text": reply["text"]})

    return jsonify(reply)

# Return chat history
@app.route("/history", methods=["GET"])
def history():
    user_id = session.get("user_id")
    if user_id not in user_chats:
        user_chats[user_id] = []
    return jsonify(user_chats[user_id])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

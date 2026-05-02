import json
import os
import random

def calculate_probability(score, budget_raw, field):
    prob = 0
    if "Hot" in score: prob = 80
    elif "Warm" in score: prob = 50
    else: prob = 20
    try:
        budget = int(''.join(filter(str.isdigit, str(budget_raw))))
        if budget > 100000: prob += 10
    except: pass
    return min(max(prob, 0), 99)

def generate_body(name, field, score, budget):
    first_name = name.split()[0] if name else "there"
    try:
        clean_b = int(''.join(filter(str.isdigit, str(budget))))
        formatted_budget = f"₹{clean_b:,}"
    except:
        formatted_budget = str(budget)
        clean_b = 0

    # Benefit strings based on field for variety
    benefit_map = {
        "AI Agent": [
            "AI agents are no longer a luxury; they are a fundamental shift in how businesses scale operations 24/7.",
            "In today's market, custom AI agents are the ultimate competitive advantage for operational efficiency.",
            "The ability to automate decision-making with AI is the bridge between a good business and a scalable empire."
        ],
        "Digital Marketing": [
            "The digital landscape is competitive, but a data-driven strategy can turn your marketing into a high-ROI engine.",
            "Modern digital marketing is about precision and timing, and I see huge potential in your current field.",
            "Scaling your brand presence through strategic digital marketing is the fastest way to drive measurable growth."
        ]
    }

    field_key = next((k for k in benefit_map.keys() if k in field), "Automation")
    benefit = random.choice(benefit_map.get(field_key, ["Strategic automation is the key to removing manual bottlenecks and focusing on high-level growth."]))

    calendly = "https://calendly.com/sharmashikhar20/book-1-1-clarity-call"
    signature = "Best regards,\n\nShikhar Sharma\nYour AI Companion"

    if "Hot" in score and "Semi" not in score:
        intros = [
            f"I was reviewing your inquiry regarding {field} and I'm very impressed with the vision you've outlined.",
            f"Thank you for reaching out about {field}. The scope you've described looks incredible.",
            f"I've just analyzed your requirements for {field}, and I'm genuinely excited about the scale we can achieve here."
        ]
        intro = random.choice(intros)
        message = f"{intro}\n\nWith a budget of {formatted_budget}, we have the perfect foundation to build a truly robust, production-grade system. {benefit}\n\nI'm dedicated to personally leading the development of your project and ensuring every detail is optimized for your success."
        cta = f"Let's connect for a 30-minute strategy call to discuss the roadmap. You can pick a time that works best for you here:\n{calendly}"

    elif "Semi-Hot" in score:
        message = f"Thank you for reaching out about {field}. I've had a chance to look over your requirements, and while a budget of {formatted_budget} is a good starting point, I'd love to discuss how we can maximize the long-term impact.\n\nBy scaling the investment slightly, we can unlock significantly more advanced AI features that provide a much higher return on investment. {benefit}\n\nI specialize in high-performance builds and want to make sure you get the absolute best results possible from this technology."
        cta = f"I'd love to jump on a quick call to explain the difference in impact between various build tiers. Please grab a slot here:\n{calendly}"

    elif "Warm" in score:
        message = f"Thanks for your interest in {field}! Your budget of {formatted_budget} is a fantastic starting point for us to prove the value of this technology. {benefit}\n\nI personally build these systems to bridge the gap between idea and execution, and I'd love to see how I can help you scale your business."
        cta = f"Would you like to hop on a 1-on-1 clarity call to discuss the next steps? You can book a time here:\n{calendly}"

    else:
        message = f"Thanks for reaching out! It's great to see your interest in {field}. Even starting with a budget of {formatted_budget}, there are several ways we can begin building a high-impact foundation for your business. {benefit}\n\nI specialize in developing custom AI agents. If you're ready to see how we can make this work for you, feel free to book a time to chat:"
        cta = f"Book your clarity call here:\n{calendly}"

    return f"Hi {first_name},\n\n{message}\n\n{cta}\n\n{signature}"

def main():
    if not os.path.exists(".tmp/scored_leads.json"): return

    with open(".tmp/scored_leads.json", "r") as f:
        data = json.load(f)

    values = data["values"]
    headers = values[0]
    idx = {h.lower().strip(): i for i, h in enumerate(headers)}

    outreach_entries = []
    for row in values[1:]:
        try:
            name, email, budget, field, score = row[idx['name']], row[idx['email']], row[idx['budget']], row[idx['field of work']], row[idx['score']]
            prob = calculate_probability(score, budget, field)
            body = generate_body(name, field, score, budget)
            outreach_entries.append({
                "name": name, "email": email, "probability": f"{prob}%",
                "subject": f"Revolutionizing your {field} strategy", "body": body,
                "budget": budget, "field": field, "score": score
            })
        except: pass

    with open(".tmp/outreach_drafts.json", "w") as f:
        json.dump(outreach_entries, f, indent=2)
    print(f"Generated {len(outreach_entries)} personalized outreach drafts.")

if __name__ == "__main__":
    main()

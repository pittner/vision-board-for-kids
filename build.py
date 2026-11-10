#!/usr/bin/env python3
"""Builds index.html for pittner/vision-board-for-kids.

A single-purpose page for the "vision board for kids" intent (parents and teachers, New Year 2027):
36 kid-friendly goals in 6 groups, each with why it matters and a first step; one click opens the free
maker prefilled. Plus 12 questions, a 45-minute plan, a box for your own goal, and FAQ.
"""
import html as _html
import json
import pathlib
from urllib.parse import urlencode

HERE = pathlib.Path(__file__).resolve().parent
URL = "https://pittner.github.io/vision-board-for-kids/"
SRC = "ghpages_kids"
CAMPAIGN = "kids_2027"

# (group, [(goal, why it matters, a first step for this week)])
GROUPS = [
    ("School and learning", [
        ("Read 20 books this year", "Kids who read a little every day find reading easy instead of hard.", "Pick the next book together and read 10 pages tonight"),
        ("Get better at maths", "Small daily practice turns a scary subject into a game.", "Do 5 minutes of times tables or a maths app after school"),
        ("Learn to write in joined-up letters", "Neat writing makes schoolwork faster and kids prouder of it.", "Copy one short sentence slowly every evening this week"),
        ("Ask one question in class every day", "Asking is how kids learn that not knowing is normal.", "Agree on one question to ask tomorrow before bedtime"),
        ("Finish homework before screen time", "A simple order removes daily arguments about homework.", "Write the rule on a sticky note by the screen"),
        ("Learn a few words in another language", "A second language opens a door to new friends and places.", "Learn how to say hello, thank you and goodbye this week"),
    ]),
    ("Healthy body", [
        ("Learn to ride a bike", "Riding a bike gives kids freedom and confidence.", "Practise balancing for 10 minutes in a park this weekend"),
        ("Learn to swim", "Swimming is a skill for safety and for fun for life.", "Book one lesson or go to the pool together"),
        ("Eat a fruit or vegetable with every meal", "Habits made in childhood are the ones that last.", "Let your child choose one new fruit at the shop"),
        ("Go to bed on time", "Good sleep makes school, sport and moods easier.", "Set a bedtime and a 10-minute wind-down routine tonight"),
        ("Try a new sport", "A first try costs little and might become a passion.", "Find one free trial training nearby"),
        ("Play outside every day", "Outdoor play builds strength, focus and good mood.", "Plan 30 minutes outside after school tomorrow"),
    ]),
    ("Friends and family", [
        ("Make a new friend", "One new friend can change how a child feels about school.", "Invite one classmate to play this week"),
        ("Help at home every day", "Small jobs teach kids that they matter to the family.", "Choose one daily job: setting the table, feeding the pet or watering plants"),
        ("Be kind to my brother or sister", "Kindness at home is the easiest place to practise it.", "Do one nice thing for a sibling today without being asked"),
        ("Call grandma and grandpa every week", "Grandparents remember these calls more than any gift.", "Pick a day and time for a weekly call"),
        ("Have a family game night", "Playing together builds memories and teaches how to lose well.", "Choose a game and put the first night in the calendar"),
        ("Say sorry and thank you more", "Two small words make friendships last.", "Notice and say one thank-you at dinner every day"),
    ]),
    ("Creative and fun", [
        ("Learn to draw animals", "Drawing builds patience and shows progress you can see.", "Draw one animal a day and keep them in one folder"),
        ("Build something big from LEGO or boxes", "Big builds teach planning and finishing what you start.", "Pick the project and collect the pieces in one box"),
        ("Learn to play an instrument", "Ten minutes a day beats one long lesson a month.", "Play for 10 minutes today, even just one song"),
        ("Write and illustrate my own story", "A finished little book makes a child feel like an author.", "Fold paper into a booklet and write the first page"),
        ("Put on a show for the family", "Performing at home builds courage for school presentations.", "Choose the date and what the show will be"),
        ("Learn a magic trick", "One trick shown to friends gives a big confidence boost.", "Watch one simple card trick and practise it 5 times"),
    ]),
    ("Brave and kind", [
        ("Speak up when something is wrong", "Kids who speak up protect themselves and others.", "Practise one sentence to use when something feels wrong"),
        ("Try one new food each month", "Being brave with small things makes big things easier.", "Pick this month's new food together"),
        ("Help someone who needs it", "Helping makes kids feel capable and good inside.", "Find one small way to help a neighbour or classmate this week"),
        ("Give toys I don't use to other kids", "Giving shows kids how much they already have.", "Choose three toys together and decide where they go"),
        ("Do something I'm scared of", "Each brave step makes the next one smaller.", "Name one small fear and plan a tiny first step"),
        ("Look after a plant or pet", "Caring for something living teaches responsibility.", "Plant one seed in a pot and water it every morning"),
    ]),
    ("Money and dreams", [
        ("Save money for something I really want", "Saving teaches that waiting brings bigger rewards.", "Draw the thing, write the price and start a jar"),
        ("Earn my first money", "Earning shows kids that money comes from effort.", "Agree on one extra job at home with a small reward"),
        ("Visit a place I've always wanted to see", "A dream trip gives the whole year something to look forward to.", "Find the place on a map and stick a picture on the fridge"),
        ("Know what I want to be when I grow up", "Dreaming about jobs helps kids see what they love.", "Talk about three jobs that sound fun and why"),
        ("Keep my room tidy", "A tidy room makes it easier to find things and to relax.", "Do a 5-minute tidy-up before bed tonight"),
        ("Finish a full year of my goals", "Looking back at a year of small wins builds real self-belief.", "Put the board where your child sees it every morning"),
    ]),
]

QUESTIONS = [
    "What made you really happy this year?",
    "What do you want to learn to do by yourself?",
    "Which sport or game would you like to try?",
    "Who would you like to spend more time with?",
    "What is something you are a little scared of but want to try?",
    "Where would you love to go?",
    "What would you like to be better at in school?",
    "What do you want to make or build?",
    "How can you help at home or at school?",
    "What would you save money for?",
    "What would make you proud of yourself next year?",
    "If you could pick only three goals, which would they be?",
]

PLAN = [
    ("10 minutes: talk and dream.", "Sit together with paper and ask what they want to do, learn or try next year. Write every idea down, no judging."),
    ("10 minutes: answer the questions.", "Go through the 12 questions below out loud. Short answers are fine; younger kids can draw instead."),
    ("10 minutes: pick three goals.", "Choose three together: one for school, one for fun, one for being kind or brave. Give each a first step."),
    ("15 minutes: make it visible.", "Turn each goal into a picture card to print or a tablet lock screen, and hang the board where your child sees it every morning."),
]

FAQ = [
    ("What should kids put on a vision board?",
     "Goals they chose themselves: things to learn, sports to try, friends and family, brave and kind acts, and something to save for. "
     "This page has 36 kid-friendly goals in 6 groups (school and learning, healthy body, friends and family, creative and fun, brave and kind, money and dreams), each with a first step for this week."),
    ("What age is a vision board good for?",
     "From about age 5 with pictures and parent help, and on their own from about age 8. Teens can use the same goals with their own words."),
    ("How do I make a vision board with my child?",
     "Talk first, then pick three goals, write each with one small first step, and put the board where your child sees it every day, like the fridge or bedroom door."),
    ("Can teachers use this in class?",
     "Yes. Each child picks goals from the list, makes a card in the free maker and prints it. It works well for New Year or back-to-school lessons."),
    ("Is the maker free?",
     "Yes. It runs in your browser, needs no account and uploads nothing. Save the image or print it."),
    ("Can we make a full picture vision board?",
     "Yes. Start from your goals in the AI vision board generator: you see a free preview, and unlocking the full-size board is optional (8.99 EUR)."),
]

def e(s):
    return _html.escape(s, quote=True)


def link(path, **extra):
    q = dict(extra)
    q.update({"utm_source": SRC, "utm_medium": "referral", "utm_campaign": CAMPAIGN})
    return "https://visionboard.bemooore.com" + path + "?" + urlencode(q)


def maker(goal, step, content):
    return link("/free-vision-board-maker/", goal=goal, step=step, layout="text", mode="wallpaper", utm_content=content)


TOOL = link("/free-vision-board-maker/", mode="wallpaper", layout="text", utm_content="plan_tool")
AI = link("/en/create.php", utm_content="faq_ai")
AI_PLAN = link("/en/create.php", utm_content="plan_ai")
HOME = link("/", utm_content="footer_home")


def slug(s):
    return "-".join("".join(c if c.isalnum() else " " for c in s.lower()).split())


def build():
    count = sum(len(gs) for _, gs in GROUPS)
    nav = " ".join(f'<a class="chip" href="#{slug(g)}">{e(g)}</a>' for g, _ in GROUPS)
    blocks = []
    for g, goals in GROUPS:
        cards = []
        for i, (goal, why, step) in enumerate(goals, 1):
            cid = f"{slug(g)}_{i}"
            cards.append(
                f'      <div class="wcard" id="g-{cid}"><h3>{e(goal)}</h3><p>{e(why)}</p>'
                f'<p class="step"><span>First step this week:</span> {e(step)}</p>'
                f'<a class="btn" href="{e(maker(goal, step, "goal_" + cid))}" data-cta="goal_{cid}">Make it my lock screen</a></div>')
        blocks.append(f'  <section class="grp" id="{slug(g)}">\n    <h2>{e(g)}</h2>\n    <div class="grid">\n'
                      + "\n".join(cards) + "\n    </div>\n  </section>")
    questions = "\n".join(f"    <li>{e(q)}</li>" for q in QUESTIONS)
    plan = "\n".join(f"    <li><b>{e(a)}</b> {e(b)}</li>" for a, b in PLAN)
    faq_html = "\n".join(f"  <h3>{e(q)}</h3>\n  <p>{e(a)}</p>" for q, a in FAQ)
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
        ensure_ascii=False)
    page = TEMPLATE
    for k, v in {
        "%%NAV%%": nav, "%%GROUPS%%": "\n\n".join(blocks), "%%QUESTIONS%%": questions, "%%PLAN%%": plan,
        "%%FAQ%%": faq_html, "%%LD%%": ld, "%%COUNT%%": str(count), "%%NQ%%": str(len(QUESTIONS)),
        "%%TOOL%%": e(TOOL), "%%AI%%": e(AI), "%%AIPLAN%%": e(AI_PLAN), "%%HOME%%": e(HOME),
        "%%URL%%": URL, "%%SRC%%": SRC, "%%CAMPAIGN%%": CAMPAIGN,
    }.items():
        page = page.replace(k, v)
    (HERE / "index.html").write_text(page, encoding="utf-8")
    print("index.html", len(page.encode()), "bytes,", count, "goals")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vision Board for Kids 2027: %%COUNT%% Goal Ideas with a First Step + Free Printable Maker</title>
<meta name="description" content="%%COUNT%% vision board ideas for kids (school, healthy body, friends and family, creative, brave and kind, money and dreams), each with a first step, %%NQ%% questions to ask your child and a 45-minute plan. Free maker, print or save.">
<link rel="canonical" href="%%URL%%">
<meta property="og:type" content="website">
<meta property="og:title" content="Vision board for kids 2027 - %%COUNT%% goal ideas with a first step and a free maker">
<meta property="og:description" content="Kid-friendly goals for school, sport, friends and kindness with a first step, %%NQ%% questions, and a printable card in one click. Free, no signup.">
<meta property="og:url" content="%%URL%%">
<style>
:root{--ink:#111827;--muted:#6B7280;--rule:#E5E7EB;--acc:#1D4ED8;--bg:#F8FAFD}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
a{color:var(--acc)}
.wrap{max-width:1000px;margin:0 auto;padding:0 20px}
header.hero{padding:48px 0 18px}
h1{font:600 clamp(28px,4.4vw,42px)/1.15 Georgia,"Times New Roman",serif;margin:0 0 14px;letter-spacing:-.01em}
.lede{font-size:18px;color:#374151;max-width:64ch;margin:0 0 14px}
.meta{font-size:14px;color:var(--muted);margin:0}
.btn{appearance:none;display:inline-block;text-decoration:none;border:1px solid #D1D5DB;background:#fff;color:var(--ink);padding:9px 15px;border-radius:999px;font:500 14px/1 inherit;cursor:pointer}
.btn:hover{border-color:var(--acc);color:var(--acc)}
.btn.primary{background:var(--acc);border-color:var(--acc);color:#fff}
.btn.primary:hover{background:#1E40AF;color:#fff}
.own{background:#fff;border:1px solid var(--rule);border-radius:16px;padding:18px;margin:8px 0 22px}
.own h2{font:600 21px/1.3 Georgia,serif;margin:0 0 10px}
.own .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.3fr) auto;gap:8px;align-items:end}
@media (max-width:760px){.own .row{grid-template-columns:1fr}}
.own label{display:block;font-size:13px;color:var(--muted);margin:0 0 4px}
.own input{width:100%;border:1px solid #D1D5DB;border-radius:10px;padding:10px 12px;font:16px/1.3 inherit;background:#fff}
.own input:focus{outline:2px solid var(--acc);outline-offset:1px;border-color:var(--acc)}
#ownMsg{font-size:13px;color:var(--muted);margin:8px 0 0}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 6px}
.chip{display:inline-block;text-decoration:none;border:1px solid var(--rule);background:#fff;color:#374151;padding:6px 12px;border-radius:999px;font-size:14px}
.chip:hover{border-color:var(--acc);color:var(--acc)}
section.grp{padding:22px 0 8px}
section.grp h2{font:600 24px/1.25 Georgia,serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
@media (max-width:860px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:520px){.grid{grid-template-columns:1fr}}
.wcard{background:#fff;border:1px solid var(--rule);border-radius:14px;padding:14px 14px 16px;display:flex;flex-direction:column}
.wcard h3{font:600 19px/1.25 Georgia,serif;margin:0 0 6px}
.wcard p{margin:0 0 8px;color:#374151;font-size:15px}
.wcard .step{font-size:14px;color:var(--muted);flex:1}
.wcard .step span{color:var(--acc);font-weight:600}
.wcard .btn{align-self:flex-start}
section.block{padding:30px 0;border-top:1px solid var(--rule);margin-top:20px}
section.block h2{font:600 24px/1.25 Georgia,serif;margin:0 0 8px}
section.block>p{max-width:70ch;color:#374151}
ol.how,ol.qs{max-width:70ch;color:#374151;padding-left:22px}
ol.how li,ol.qs li{margin:0 0 10px}
.faq h3{font:600 16px/1.4 inherit;margin:18px 0 4px}
.faq p{margin:0;color:#374151;max-width:70ch}
footer{padding:28px 0 60px;font-size:14px;color:var(--muted);border-top:1px solid var(--rule)}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <h1>Vision board for kids 2027: %%COUNT%% goal ideas, each with a first step for this week</h1>
  <p class="lede">A vision board helps kids turn wishes into small steps they can see every day. Below are %%COUNT%% vision board ideas for kids, from learning to ride a bike and reading 20 books to saving for something special and being brave, each with why it matters and a first step for this week, plus %%NQ%% questions to ask your child. Press a goal and it opens in a free maker: print it for the fridge or bedroom door, or save it as a tablet lock screen. Works for parents at home and teachers in class.</p>
  <p class="meta">%%COUNT%% goals in 6 groups &middot; %%NQ%% questions &middot; 45-minute plan &middot; lock screen in one click &middot; free, MIT licensed</p>
</header>

<div class="own" id="own">
  <h2>Already know your goal?</h2>
  <div class="row">
    <div><label for="ownGoal">My child's goal for 2027</label><input id="ownGoal" maxlength="120" placeholder="e.g. Learn to ride a bike by summer" autocomplete="off"></div>
    <div><label for="ownStep">First step (optional)</label><input id="ownStep" maxlength="120" placeholder="e.g. Practise 10 minutes on Saturday" autocomplete="off"></div>
    <button class="btn primary" id="ownGo" type="button">Make it my lock screen</button>
  </div>
  <p id="ownMsg">Opens the free maker with your goal filled in. Change colors or layout there, then save it to your phone or print it.</p>
</div>

<nav class="chips" aria-label="Groups">%%NAV%% <a class="chip" href="#questions">%%NQ%% questions</a> <a class="chip" href="#plan">45-minute plan</a></nav>

%%GROUPS%%

<section class="block" id="questions">
  <h2>%%NQ%% questions to ask your child</h2>
  <p>Ask them out loud in 15 minutes. Younger kids can answer with a drawing. The answers that make them smile point to goals they will actually want to work on.</p>
  <ol class="qs">
%%QUESTIONS%%
  </ol>
</section>

<section class="block" id="plan">
  <h2>Make a kids vision board together in 45 minutes</h2>
  <ol class="how">
%%PLAN%%
  </ol>
  <p><a class="btn primary" href="%%TOOL%%" data-cta="plan_tool">Open the free lock-screen maker</a>
     <a class="btn" href="%%AIPLAN%%" data-cta="plan_ai">Make a full board with all my goals</a></p>
</section>

<section class="block faq">
  <h2>Questions</h2>
%%FAQ%%
  <p style="margin-top:16px"><a class="btn" href="%%AI%%" data-cta="faq_ai">Make a full picture vision board for my child</a></p>
</section>

<footer>
  MIT licensed &middot; published by the team behind
  <a href="%%HOME%%" data-cta="footer_home">visionboard.bemooore.com</a> &middot;
  more: <a href="https://pittner.github.io/bucket-list-vision-board/">bucket list vision board</a>,
  <a href="https://pittner.github.io/manifestation-vision-board/">manifestation vision board</a>,
  <a href="https://pittner.github.io/dream-home-vision-board/">dream home vision board</a>,
  <a href="https://pittner.github.io/fitness-vision-board/">fitness vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-relationships/">relationships vision board</a>,
  <a href="https://pittner.github.io/travel-vision-board/">travel vision board</a>,
  <a href="https://pittner.github.io/self-care-vision-board/">self care vision board</a>,
  <a href="https://pittner.github.io/money-vision-board/">money vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-weight-loss/">weight loss vision board</a>,
  <a href="https://pittner.github.io/new-year-resolutions-2027/">new year's resolutions 2027</a>,
  <a href="https://pittner.github.io/vision-board-for-career/">career vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-family/">family vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-couples/">vision board for couples</a>,
  <a href="https://pittner.github.io/vision-board-for-small-business/">small business vision board</a>,
  <a href="https://pittner.github.io/vision-board-for-students/">vision board for students</a>,
  <a href="https://pittner.github.io/word-of-the-year-2027/">word of the year 2027</a>,
  <a href="https://pittner.github.io/2027-vision-board-template/">printable 2027 vision board template</a>,
  <a href="https://pittner.github.io/vision-board-prompts/">54 vision board prompts</a>,
  <a href="https://pittner.github.io/">all free tools</a> &middot;
  <a href="https://github.com/pittner/vision-board-for-kids">source</a>
</footer>
</div>

<script type="application/ld+json">
%%LD%%
</script>

<script>
(function(){
  var EP='https://visionboard.bemooore.com/api/event.php',P='%%SRC%%',engaged=false;
  function beacon(ev,label){
    try{
      var b=JSON.stringify({event:ev,utm:P+' | '+label+' | '+location.search});
      if(navigator.sendBeacon){navigator.sendBeacon(EP,new Blob([b],{type:'text/plain'}));}
      else{fetch(EP,{method:'POST',body:b,keepalive:true,mode:'no-cors'});}
    }catch(e){}
  }
  // Every link to our site carries where the visitor came from (e.g. chatgpt.com).
  var src=(location.search.match(/[?&]utm_source=([^&]+)/)||[])[1]||(document.referrer?document.referrer.split('/')[2]:'direct');
  Array.prototype.forEach.call(document.querySelectorAll('a[data-cta][href*="visionboard.bemooore.com"]'),function(a){
    a.href+='&utm_term='+encodeURIComponent('via_'+src);
  });
  function engage(how){ if(engaged)return; engaged=true; beacon('page_engaged',how); }
  setTimeout(function(){engage('dwell6s');},6000);
  window.addEventListener('scroll',function(){
    var h=document.documentElement;
    if((h.scrollTop||document.body.scrollTop)/((h.scrollHeight-h.clientHeight)||1)>0.25) engage('scroll25');
  },{passive:true});
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-cta]'); if(a) beacon('cta_click',a.getAttribute('data-cta'));
  });

  // Own goal: same prefill as the goal cards (?goal=&step=&layout=text&mode=wallpaper).
  var g=document.getElementById('ownGoal'),s=document.getElementById('ownStep'),msg=document.getElementById('ownMsg');
  function go(){
    var goal=g.value.trim(),step=s.value.trim();
    if(!goal){ msg.textContent='Type your goal first.'; g.focus(); return; }
    var q=new URLSearchParams({goal:goal,layout:'text',mode:'wallpaper',utm_source:P,utm_medium:'referral',
      utm_campaign:'%%CAMPAIGN%%',utm_content:'own_goal',utm_term:'via_'+src});
    if(step) q.set('step',step);
    beacon('cta_click','own_goal');
    location.href='https://visionboard.bemooore.com/free-vision-board-maker/?'+q.toString();
  }
  document.getElementById('ownGo').addEventListener('click',go);
  [g,s].forEach(function(el){ el.addEventListener('keydown',function(e){ if(e.key==='Enter') go(); }); });
})();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    build()

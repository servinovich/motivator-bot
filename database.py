import sqlite3

DB_NAME = "motivations.db"

def init_db():
    """Создает таблицу в базе данных, если её нет"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS motivations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trigger TEXT,
            response TEXT
        )
    """)
    
    conn.commit()
    conn.close()

import random

def get_motivation(trigger, last_response=None):
    """Ищет мотивацию по ключевому слову и исключает последний ответ"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    words = trigger.lower().split()
    matched_responses = []

    for word in words:
        cursor.execute("SELECT response FROM motivations WHERE LOWER(trigger) LIKE LOWER(?)", (f"%{word}%",))
        results = cursor.fetchall()  # Получаем ВСЕ возможные совпадения
        matched_responses.extend([row[0] for row in results])

    conn.close()

    if not matched_responses:
        return None  # Если ничего не найдено, возвращаем None

    # Исключаем предыдущий ответ, если он есть
    if last_response in matched_responses:
        matched_responses.remove(last_response)

    # Если остались варианты, выбираем случайный
    if matched_responses:
        return random.choice(matched_responses)

    return last_response  # Если удалили единственную фразу, возвращаем её снова

def add_default_motivations():
    """Добавляет стандартные мотивационные фразы в базу"""
    motivations = [
("wake up, morning, start day, get out of bed, overslept", "You wasted half the day, but you don’t have to waste the rest. Get up and take control."),
("tired, exhausted, fatigue, no energy, drained", "Your body is tired, but your mind is weak. Strength comes from pushing through."),
("failure, lost, mistake, setback, unsuccessful", "Failure is the best lesson life gives you. Winners learn, losers quit."),
("lazy, procrastination, wasting time, unproductive, postponing", "Every second you waste, someone else is working. Get up and move."),
("fear, scared, anxiety, hesitation, doubt", "Fear is the excuse of the weak. If you want to win, face it head-on."),
("success, win, achieve, reach goal, victory", "Success is never given, it’s taken. Are you taking what’s yours?"),
("confidence, self-belief, self-esteem, self-worth, assurance", "Confidence isn’t something you wait for, it’s something you build. Do the work."),
("focus, concentration, discipline, no distractions, clarity", "Distraction is the enemy. Lock in and execute."),
("hard work, effort, persistence, grinding, determination", "Hard work isn’t a choice. It’s the only way."),
("struggle, tough times, adversity, hard days, resilience", "Struggle is where the real men are made. If you’re struggling, good."),
("excuses, weak mindset, complaining, justification, blaming", "Your excuses won’t make you rich, won’t make you strong, won’t make you a winner. You can have excuses, or you can have results. Never both."),
("discipline, self-control, habit, consistency, willpower", "Motivation is useless. Discipline is what separates winners from losers."),
("gym, workout, fitness, training, exercise, weightlifting", "Your body is the reflection of your mind. Weak body, weak mind."),
("training, practice, improving, repetition, mastery", "If you’re not training, you’re losing. Simple as that."),
("pain, suffering, discomfort, hardship, endurance", "Pain is the universe telling you to harden the f*** up."),
("regret, missed opportunities, wasted time, second chances, hindsight", "Live in a way where regret is never an option."),
("winners, champions, success-driven, high achievers, overachievers", "Winners don’t have backup plans. They just win."),
("weakness, fragility, insecurity, self-doubt, vulnerability", "Weakness is a disease. Cure it with action."),
("money, wealth, rich, financial success, prosperity", "Money follows power. Become powerful, and money will chase you."),
("power, strength, authority, control, dominance", "Power is earned, never given."),
("respect, admiration, dignity, reputation, recognition", "If you have to ask for respect, you don’t deserve it."),
("women, dating, relationships, attraction, romance", "A man without purpose is a toy to a woman."),
("comfort, easy life, relaxation, stagnation, mediocrity", "Comfort is killing you. Get uncomfortable and grow."),
("leadership, influence, dominance, command, control", "Real men lead. If you're not leading, you’re following."),
("hustle, grind, work hard, never stop, ambition", "No one is coming to save you. Hustle or stay broke."),
("mindset, mentality, way of thinking, attitude, approach", "Your mind is either your greatest weapon or your biggest weakness."),
("time, productivity, wasting hours, schedule, efficiency", "Time doesn’t care about your feelings. Use it or lose it."),
("strength, power, endurance, toughness, resilience", "Physical strength means nothing without mental toughness."),
("discipline over desire, commitment, self-discipline, willpower, drive", "Winners do what they must, not what they feel like."),
("sacrifice, giving up, priorities, commitment, trade-off", "Greatness demands sacrifice. Pay the price."),
("grind, push forward, effort, keep going, never stop", "Grinding today builds your future. Don’t stop."),
("motivation, inspiration, drive, purpose, passion", "Forget motivation. Train your mind to execute."),
("vision, future, long-term goals, ambition, foresight", "If you can’t see where you’re going, how do you expect to get there?"),
("responsibility, accountability, own your life, self-reliance, ownership", "No one is responsible for your success except you."),
("self-respect, dignity, self-worth, integrity, pride", "A man with no self-respect is already defeated."),
("pressure, stress, expectations, challenge, demands", "Pressure creates diamonds. Or it crushes you."),
("ambition, big dreams, life goals, determination, persistence", "Your ambition should scare the weak. Set goals beyond limits."),
("failure, learning, lessons, growth, mistakes", "Your failures are proof that you're trying. Keep pushing forward."),
("dedication, perseverance, commitment, endurance, consistency", "Stay dedicated, stay relentless, and you'll achieve what others only dream of."),
("opportunity, chances, luck, taking risks, seizing the moment", "Opportunities don’t come to those who wait, but to those who chase."),
("growth mindset, improvement, self-betterment, continuous learning, evolving", "If you’re not growing, you’re dying. Every day is a chance to improve."),
("determination, resilience, never give up, strong will, grit", "The strongest warriors are forged in the hottest fires."),
("overcoming obstacles, endurance, struggle, persistence, triumph", "Obstacles exist to be conquered, not to stop you."),
("courage, bravery, facing fears, taking risks, fearless", "Courage is doing what scares you. Fear is an illusion."),
("self-improvement, learning, evolving, adaptation, leveling up", "If you’re the same person you were a year ago, you’ve failed."),
("mental toughness, fortitude, indomitable spirit, inner strength, mindset shift", "Your mind is your strongest muscle. Train it daily."),
("independence, self-sufficiency, standing alone, autonomy, control", "The strongest men stand alone and lead others forward."),
("work ethic, putting in effort, non-stop grind, consistency, daily action", "Your work ethic determines your future. Be relentless."),
("adaptability, flexibility, problem-solving, overcoming adversity, adjusting", "Adapt or perish. The world doesn’t wait for the weak."),
("boldness, daring, taking initiative, leading the way, fearless decisions", "Be bold. Take the risk. Weakness hesitates, strength executes."),
("execution, finishing what you start, action-taking, no hesitation, results", "Winners execute. Dreamers wait. Which one are you?"),
("overcome fear, face challenges, be fearless, conquer doubts", "Fear is the greatest enemy of progress. Face it, fight it, and move forward."),
("success mindset, unstoppable, no limits, think big, achieve greatness", "The only limits you have are the ones you accept. Break them and rise."),
("grind, never stop, push forward, keep going, persistence", "The grind doesn’t care about your feelings. Show up and get it done."),
("discipline, habits, daily improvement, small wins, self-mastery", "Small daily improvements lead to massive success over time. Stay disciplined."),
("focus, eliminate distractions, lock in, deep work, stay sharp", "Success is the result of extreme focus. Cut out the noise and lock in."),
("resilience, mental strength, never quit, endure, stand strong", "Pain is temporary, but quitting lasts forever. Keep going."),
("self-confidence, self-belief, trust yourself, inner power, own it", "The world will doubt you, but you must never doubt yourself."),
("power moves, take control, be the leader, step up, make decisions", "Leaders don’t wait for permission. They take action."),
("hard times, struggle, adversity, test of strength, prove yourself", "Hard times create strong men. If you’re struggling, you’re growing."),
("execution, taking action, stop waiting, move fast, results-driven", "Thinking won’t change your life. Execution will. Take action now."),
]

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for trigger, response in motivations:
        cursor.execute("SELECT 1 FROM motivations WHERE trigger = ? AND response = ?", (trigger, response))
        if not cursor.fetchone():  # Проверяем, есть ли уже такая запись
            cursor.execute("INSERT INTO motivations (trigger, response) VALUES (?, ?)", (trigger, response))

    conn.commit()
    conn.close()

# Cлучайная мотивация
def get_random_motivation():
    """Выбирает случайную мотивационную фразу, если точного совпадения нет"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT response FROM motivations ORDER BY RANDOM() LIMIT 1")
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else "Keep pushing forward! Your breakthrough is coming."

# Инициализируем базу при первом запуске
init_db()
add_default_motivations()  # Запускаем добавление стандартных мотивационных фраз

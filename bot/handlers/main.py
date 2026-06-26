from bot.dp import dp
from bot.buttons.inline import week_menu
from aiogram.types import CallbackQuery, Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from bot.db.database import SessionLocal
from bot.db.models import Lesson
from bot.states.lesson_state import LessonState


# ── Dars qo'shish ──────────────────────────────────────
@dp.message(F.text == "➕ Dars qo'shish")
async def add_lesson(message: Message, state: FSMContext):
    await message.answer("Qaysi kun? (monday, tuesday, wednesday, thursday, friday, saturday)")
    await state.set_state(LessonState.day)

@dp.message(LessonState.day)
async def get_day(message: Message, state: FSMContext):
    await state.update_data(day=message.text.lower())
    await message.answer("Qaysi fan?")
    await state.set_state(LessonState.subject)

@dp.message(LessonState.subject)
async def get_subject(message: Message, state: FSMContext):
    data = await state.get_data()
    session = SessionLocal()
    session.add(Lesson(day=data["day"], subject=message.text))
    session.commit()
    session.close()
    await message.answer("✅ Dars muvaffaqiyatli qo'shildi.")
    await state.clear()


# ── Darsni o'zgartirish ────────────────────────────────
@dp.message(F.text == "✏️ Darsni o'zgartirish")
async def edit_lesson(message: Message, state: FSMContext):
    await message.answer("Qaysi kun darsini o'zgartirasiz? (monday, tuesday...)")
    await state.set_state(LessonState.edit_day)

@dp.message(LessonState.edit_day)
async def get_edit_day(message: Message, state: FSMContext):
    await state.update_data(day=message.text)
    await message.answer("Yangi fan nomini kiriting:")
    await state.set_state(LessonState.edit_subject)

@dp.message(LessonState.edit_subject)
async def update_subject(message: Message, state: FSMContext):
    data = await state.get_data()
    session = SessionLocal()
    lesson = session.query(Lesson).filter(Lesson.day == data["day"]).first()
    if lesson:
        lesson.subject = message.text
        session.commit()
        await message.answer("✅ Dars o'zgartirildi.")
    else:
        await message.answer("❌ Bunday kun topilmadi.")
    session.close()
    await state.clear()


# ── Darsni o'chirish ───────────────────────────────────
@dp.message(F.text == "❌ Darsni o'chirish")
async def delete_lesson(message: Message, state: FSMContext):
    await message.answer("Qaysi kun darsini o'chirmoqchisiz? (monday, tuesday...)")
    await state.set_state(LessonState.delete_day)

@dp.message(LessonState.delete_day)
async def confirm_delete(message: Message, state: FSMContext):
    session = SessionLocal()
    lesson = session.query(Lesson).filter(Lesson.day == message.text).first()
    if lesson:
        session.delete(lesson)
        session.commit()
        await message.answer("✅ Dars muvaffaqiyatli o'chirildi.")
    else:
        await message.answer("❌ Bunday kun topilmadi.")
    session.close()
    await state.clear()


# ── Haftalik darslar ───────────────────────────────────
@dp.message(F.text == "📅 Haftalik darslar")
async def weekly_lessons(message: Message):
    await message.answer("Kerakli kunni tanlang:", reply_markup=week_menu)

days = {
    "monday": "📅 Dushanba",
    "tuesday": "📅 Seshanba",
    "wednesday": "📅 Chorshanba",
    "thursday": "📅 Payshanba",
    "friday": "📅 Juma",
    "saturday": "📅 Shanba",
}

from aiogram.filters import  Command

@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(f"@zzxxddab     adminga murojat uchun")

@dp.callback_query(F.data.in_(days.keys()))
async def show_day_lessons(callback: CallbackQuery):
    day = callback.data
    session = SessionLocal()
    lessons = session.query(Lesson).filter(Lesson.day == day).all()
    session.close()
    title = days[day]
    text = f"{title} darslari:\n\n" + "\n".join(f"📖 {l.subject}" for l in lessons) if lessons else f"{title}: dars topilmadi."
    await callback.message.answer(text)
    await callback.answer()
from ..app import User

def get_dashboard_data(user_id):
    user = User.query.get(user_id)
    if not user:
        return None

    # For now, recommendations are still placeholders
    recommendations = [
        "Complete the Python for Beginners course.",
        "Add 'Data Analysis' to your resume.",
        "Explore job opportunities in the 'Data Scientist' field."
    ]

    progress_data = {
        "courses_completed": user.progress.courses_completed if user.progress else 0,
        "skills_acquired": [skill.name for skill in user.skills],
        "resume_score": user.progress.resume_score if user.progress else 0
    }

    return {
        "user_id": user.id,
        "username": user.username,
        "recommendations": recommendations,
        "progress": progress_data
    }

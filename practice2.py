"""
Упрощённый Django-подобный проект в одном файле
(логически разделён на models.py, views.py, templates)
"""

# =========================
# MODELS (models.py)
# =========================

from datetime import datetime


class BaseModel:
    """Базовый класс модели (имитация Django ORM)"""
    _id_counter = 1

    def __init__(self):
        self.id = BaseModel._id_counter
        BaseModel._id_counter += 1


class Organization(BaseModel):
    """Модель организации"""

    def __init__(self, name, volunteers_count):
        super().__init__()
        self.name = name
        self.volunteers_count = volunteers_count
        self.resources = []
        self.projects = []
        self.donations = []

    def __str__(self):
        return f"Организация: {self.name}"


class Resource(BaseModel):
    """Модель ресурса"""

    def __init__(self, name, quantity, organization):
        super().__init__()
        self.name = name
        self.quantity = quantity
        self.organization = organization

    def __str__(self):
        return f"{self.name} ({self.quantity})"


class Project(BaseModel):
    """Модель проекта"""

    def __init__(self, title, description, organization):
        super().__init__()
        self.title = title
        self.description = description
        self.organization = organization

    def __str__(self):
        return self.title


class Donation(BaseModel):
    """Модель сбора пожертвований"""

    def __init__(self, title, goal_amount, organization):
        super().__init__()
        self.title = title
        self.goal_amount = goal_amount
        self.organization = organization

    def __str__(self):
        return f"{self.title} (Цель: {self.goal_amount})"


# =========================
# DATABASE (имитация БД)
# =========================

DATABASE = {
    "organizations": []
}


# =========================
# VIEWS (views.py)
# =========================

def create_organization(name, volunteers_count):
    """Создание организации"""
    org = Organization(name, volunteers_count)
    DATABASE["organizations"].append(org)
    return org


def add_resource(org, name, quantity):
    """Добавление ресурса"""
    resource = Resource(name, quantity, org)
    org.resources.append(resource)


def add_project(org, title, description):
    """Добавление проекта"""
    project = Project(title, description, org)
    org.projects.append(project)


# ===== Работа с пожертвованиями (Рівень 2) =====

def create_donation(org, title, goal_amount):
    """Создание сбора пожертвований"""
    donation = Donation(title, goal_amount, org)
    org.donations.append(donation)


def edit_donation(org, donation_id, new_title=None, new_goal=None):
    """Редактирование сбора"""
    for donation in org.donations:
        if donation.id == donation_id:
            if new_title:
                donation.title = new_title
            if new_goal:
                donation.goal_amount = new_goal
            return True
    return False


def delete_donation(org, donation_id):
    """Удаление сбора"""
    org.donations = [d for d in org.donations if d.id != donation_id]


def organization_list_view():
    """Имитация view для отображения списка организаций"""

    context = {
        "organizations": DATABASE["organizations"]
    }

    return render_template(context)


# =========================
# TEMPLATES (templates)
# =========================

def render_template(context):
    """Простейший шаблонизатор"""

    output = "\n===== СПИСОК ОРГАНИЗАЦИЙ =====\n"

    for org in context["organizations"]:
        output += f"\n{org.name}\n"
        output += f"Волонтёры: {org.volunteers_count}\n"

        # Ресурсы
        output += "Ресурсы:\n"
        for res in org.resources:
            output += f" - {res.name}: {res.quantity}\n"

        # Проекты
        output += "Проекты:\n"
        for proj in org.projects:
            output += f" - {proj.title}: {proj.description}\n"

        # Пожертвования
        output += "Сборы:\n"
        for don in org.donations:
            output += f" - {don.title} (Цель: {don.goal_amount})\n"

    return output


# =========================
# MAIN (точка входа)
# =========================

def main():
    """Основная функция"""

    # Создание организации
    org1 = create_organization("Help Ukraine", 50)

    # Добавление данных
    add_resource(org1, "Медикаменты", 100)
    add_resource(org1, "Еда", 200)

    add_project(org1, "Поддержка переселенцев", "Помощь жильём")
    add_project(org1, "Мед помощь", "Обеспечение больниц")

    # Работа с пожертвованиями
    create_donation(org1, "Сбор на медикаменты", 5000)
    create_donation(org1, "Сбор на еду", 3000)

    # Редактирование
    edit_donation(org1, 6, new_goal=6000)

    # Удаление
    delete_donation(org1, 7)

    # Отображение
    result = organization_list_view()
    print(result)


if __name__ == "__main__":
    main()
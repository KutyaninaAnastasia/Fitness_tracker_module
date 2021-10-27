class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    TRAINING_TYPE = None

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_covered_km = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_covered_km

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        average_speed = self.get_distance() / self.duration
        return average_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.TRAINING_TYPE,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    TRAINING_TYPE = 'Running'
    COEFF_CALORIE_1 = 18
    COEFF_CALORIE_2 = 20

    def get_spent_calories(self) -> float:
        # Попробовала вынести значения в константы класса,
        # но программа не проходит проверку pytest
        duration_min = self.duration * 60
        speed = self.get_mean_speed()
        formula_1 = self.COEFF_CALORIE_1 * speed - self.COEFF_CALORIE_2
        return formula_1 * self.weight / self.M_IN_KM * duration_min


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    TRAINING_TYPE = 'SportsWalking'
    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 0.029
    COEFF_SPEED = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        duration_min = self.duration * 60
        speed = self.get_mean_speed()
        formula_1 = speed ** self.COEFF_SPEED // self.height
        formula_2 = self.COEFF_CALORIE_1 * self.weight
        formula_3 = formula_1 * self.COEFF_CALORIE_2 * self.weight
        return (formula_2 + formula_3) * duration_min


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    TRAINING_TYPE = 'Swimming'
    COEFF_CALORIE_1 = 1.1
    COEFF_CALORIE_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        total_distance = self.length_pool * self.count_pool
        return total_distance / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        formula_1 = self.get_mean_speed() + self.COEFF_CALORIE_1
        return formula_1 * self.COEFF_CALORIE_2 * self.weight


TRAINING_DICT = {
    # Сделала как написано в ревью, но проверила задание.
    # Там сказано:'В теле функции должен быть словарь,
    # в котором сопоставляются коды тренировок и классы,
    # которые нужно вызвать для каждого типа тренировки'.
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training = TRAINING_DICT[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

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
        """Получить сообщение о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {round(self.duration, 3):0.3f} ч.; '
                f'Дистанция: {round(self.distance, 3):0.3f} км; '
                f'Ср. скорость: {round(self.speed, 3):0.3f} км/ч; '
                f'Потрачено ккал: {round(self.calories, 3):0.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_H: float = 60

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
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return 0

    def show_training_info(self) -> InfoMessage:
        """Показать информационное сообщение о выполненной тренировке."""
        return InfoMessage('', self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           0)


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)
        self.duration_in_minutes = self.duration * self.MIN_IN_H

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration_in_minutes)

    def show_training_info(self) -> InfoMessage:
        """Показать информационное сообщение о выполненной тренировке."""
        return InfoMessage('Running', self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.height_in_m = self.height / self.CM_IN_M
        self.duration_in_m = self.duration * self.MIN_IN_H

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                 / self.height_in_m) * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight) * self.duration_in_m)

    def show_training_info(self) -> InfoMessage:
        """Показать информационное сообщение о выполненной тренировке."""
        return InfoMessage('SportsWalking', self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_WEIGHT_MULTIPLIER: float = 1.1
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return super().get_distance()

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                + self.CALORIES_WEIGHT_MULTIPLIER)
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight * self.duration)

    def show_training_info(self) -> InfoMessage:
        """Показать информационное сообщение о выполненной тренировке."""
        return InfoMessage('Swimming', self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    return workout_types[workout_type](*data)


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

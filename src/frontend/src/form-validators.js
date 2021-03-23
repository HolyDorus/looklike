export class RegisterFormValidator {
    constructor(form) {
        this.form = form;
        this.validationErrors = [];
    }

    validate() {
        const formData = new FormData(this.form);

        this.username = formData.get('username');
        this.password = formData.get('password');
        this.passwordConfirmation = formData.get('passwordConfirmation');

        this.validateUsername();
        this.validatePassword();
        this.validatePasswordConfirmation();
        this.comparePasswords();

        return this.validationErrors;
    }

    validateUsername() {
        if (!this.username) {
            this.validationErrors.push('Поле логіну є обов\'язковим для заповнення');
            return;
        }

        const isOnlyHasAllowedCharacters = /^[a-zA-Z1-9]+$/.test(this.username);

        if (!isOnlyHasAllowedCharacters) {
            this.validationErrors.push('Логін повинен містити лише латинські літери та цифри!');
        }

        if (this.username.length < 3 || this.username.length > 30) {
            this.validationErrors.push('Логін повинен містити від трьох до тридцяти символів!');
        }
    }

    validatePassword() {
        if (!this.password) {
            this.validationErrors.push('Поле паролю є обов\'язковим для заповнення');
            return;
        }

        const reCapital = this.password.match(/[A-Z]/g);
        const reDigits = this.password.match(/[0-9]/g);

        const numberOfCapitalLetters = reCapital ? reCapital.length : 0;
        const numberOfDigits = reDigits ? reDigits.length: 0;

        if (this.password.length < 8) {
            this.validationErrors.push('Пароль повинен містити мінімум шість символів!');
        }

        if (numberOfCapitalLetters < 2) {
            this.validationErrors.push('Пароль повинен містити мінімум дві великі літери!');
        }

        if (numberOfDigits < 3) {
            this.validationErrors.push('Пароль повинен містити мінімум три цифри!');
        }
    }

    validatePasswordConfirmation() {
        if (!this.passwordConfirmation) {
            this.validationErrors.push('Поле підтвердження паролю є обов\'язковим для заповнення');
        }
    }

    comparePasswords() {
        if (this.password !== this.passwordConfirmation) {
            this.validationErrors.push('Паролі не співпадають!');
        }
    }
}


export class LoginFormValidator {
    constructor(form) {
        this.form = form;
        this.validationErrors = [];
    }

    validate() {
        const formData = new FormData(this.form);

        this.username = formData.get('username');
        this.password = formData.get('password');

        this.validateUsername();
        this.validatePassword();

        return this.validationErrors;
    }

    validateUsername() {
        if (!this.username) {
            this.validationErrors.push('Поле логіну є обов\'язковим для заповнення');
        }
    }

    validatePassword() {
        if (!this.password) {
            this.validationErrors.push('Поле паролю є обов\'язковим для заповнення');
        }
    }
}

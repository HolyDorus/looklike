export function getToken() {
    return localStorage.getItem('LOOKLIKE_JWT_TOKEN');
}

export function setToken(token) {
    localStorage.setItem('LOOKLIKE_JWT_TOKEN', token);
}

export function isAuthorized() {
    const token = getToken();

    return token && token !== 'undefined';
}

export function logOut() {
    setToken('');
}
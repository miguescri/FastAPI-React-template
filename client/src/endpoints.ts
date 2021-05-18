import API from "./API";

export function login(
    username: string,
    password: string,
    setToken: (arg0: string) => void,
    onError: () => void,
) {
    let searchParams = new URLSearchParams();
    searchParams.append('username', username);
    searchParams.append('password', password);

    fetch(API + '/token',
        {
            method: 'POST',
            mode: 'cors',
            credentials: 'include',
            body: searchParams
        })
        .then(response => {
            if (response.ok) {
                response.json().then(data => {
                    setToken(data['access_token'])
                })
            } else {
                onError()
            }
        })
}

export function signup(
    username: string,
    email: string,
    name: string,
    password: string,
    onSuccess: () => void,
    onError: () => void,
) {
    let body = {username: username, email: email, password: password, name: name}

    fetch(API + '/user',
        {
            method: 'POST',
            mode: 'cors',
            credentials: 'include',
            body: JSON.stringify(body)
        })
        .then(response => {
            if (response.ok) {
                onSuccess()
            } else {
                onError()
            }
        })
}

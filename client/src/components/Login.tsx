import React, {useState} from "react";
import API from "../API";
import MyButton from "./common/MyButton";

function Login(prop: {
    setToken: (arg0: string) => void,
}) {
    const [username, setUsername] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const [credentialsError, setCredentialsError] = useState<boolean>(false)
    let errorMessage

    if (credentialsError){
        errorMessage = <p>Wrong credentials</p>
    }

    const login = () => {
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
                        prop.setToken(data['access_token'])
                    })
                } else {
                    setCredentialsError(true)
                    setUsername('')
                    setPassword('')
                }
            })
    }

    return (
        <div>
            <p>Username</p>
            <input
                type={"text"}
                value={username}
                onChange={e => setUsername(e.target.value)}
            />
            <p>Password</p>
            <input
                type={"password"}
                value={password}
                onChange={e => setPassword(e.target.value)}
            />
            <br/>
            <MyButton
                myLabel={"Login"}
                callback={() => login()}
            />
            {errorMessage}
        </div>
    )
}

export default Login

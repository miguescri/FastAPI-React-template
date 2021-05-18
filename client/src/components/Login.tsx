import React, {useState} from "react";
import MyButton from "./common/MyButton";
import {login} from "../endpoints";

function Login(prop: {
    setToken: (arg0: string) => void,
}) {
    const [username, setUsername] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const [credentialsError, setCredentialsError] = useState<boolean>(false)
    let errorMessage

    if (credentialsError) {
        errorMessage = <p>Wrong credentials</p>
    }

    const onError = () => {
        setCredentialsError(true)
        setUsername('')
        setPassword('')
    }

    const buttonCallback = () => login(username, password, prop.setToken, onError)

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
                callback={buttonCallback}
            />
            {errorMessage}
        </div>
    )
}

export default Login

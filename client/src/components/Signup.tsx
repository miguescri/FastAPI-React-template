import React, {useState} from "react";
import MyButton from "./common/MyButton";
import {signup, signupAndLogin} from "../endpoints";

function Signup(prop: {
    setToken: (arg0: string) => void,
}) {
    const [username, setUsername] = useState<string>("")
    const [email, setEmail] = useState<string>("")
    const [name, setName] = useState<string>("")
    const [password, setPassword] = useState<string>("")
    const [credentialsError, setCredentialsError] = useState<boolean>(false)
    const [success, setSuccess] = useState<boolean>(false)
    let errorMessage
    let successMessage

    if (credentialsError) {
        errorMessage = <p>Something went wrong</p>
    }
    if (success) {
        successMessage = <p>User created successfully. You can now login</p>
    }

    const onSuccess = () => {
        setUsername('')
        setEmail('')
        setName('')
        setPassword('')
        setCredentialsError(false)
        setSuccess(true)
    }

    const onError = () => {
        setCredentialsError(true)
        setSuccess(false)
    }

    const buttonCallbackSignup = () => signup(username, email, name, password, onSuccess, onError)
    const buttonCallbackSignupAndLogin = () =>
        signupAndLogin(username, email, name, password, prop.setToken, onError, onError)

    return (
        <div>
            <p>Username</p>
            <input
                type={"text"}
                value={username}
                onChange={e => setUsername(e.target.value)}
            />
            <p>Email</p>
            <input
                type={"text"}
                value={email}
                onChange={e => setEmail(e.target.value)}
            />
            <p>Name</p>
            <input
                type={"text"}
                value={name}
                onChange={e => setName(e.target.value)}
            />
            <p>Password</p>
            <input
                type={"password"}
                value={password}
                onChange={e => setPassword(e.target.value)}
            />
            <br/>
            <MyButton
                myLabel={"Sign up"}
                callback={buttonCallbackSignup}
            />
            <MyButton
                myLabel={"Sign up and login"}
                callback={buttonCallbackSignupAndLogin}
            />
            {errorMessage}
            {successMessage}
        </div>
    )
}

export default Signup

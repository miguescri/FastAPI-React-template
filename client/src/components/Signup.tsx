import React, {useState} from "react";
import API from "../API";
import MyButton from "./common/MyButton";

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
        errorMessage = <p>Wrong credentials</p>
    }
    if (success) {
        successMessage = <p>User created successfully. You can now login</p>
    }

    const signup = () => {
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
                    setUsername('')
                    setEmail('')
                    setName('')
                    setPassword('')
                    setSuccess(true)
                } else {
                    setCredentialsError(true)
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
                callback={() => signup()}
            />
            {errorMessage}
            {successMessage}
        </div>
    )
}

export default Signup

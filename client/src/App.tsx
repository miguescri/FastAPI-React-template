import React, {useState} from 'react';
import './App.css';
import MyButton from "./components/common/MyButton";
import AuthForm from "./components/AuthForm";

function App() {
    const [token, setToken] = useState<String | null>(null)
    let component

    if (!token) {
        component = <AuthForm setToken={setToken}/>
    } else {
        component = (
            <div>
                <header className="App-header">
                    <MyButton
                        myLabel={"Logout"}
                        callback={() => setToken(null)}
                    />
                    <p>You are logged in</p>
                </header>
                <p>JWT token: <code>{token}</code></p>
            </div>
        )
    }

    return (
        <div className="App">
            {component}
        </div>
    );
}

export default App;

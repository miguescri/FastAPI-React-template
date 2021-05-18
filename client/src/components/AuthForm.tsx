import React, {useState} from "react";
import MyButton from "./common/MyButton";
import Login from "./Login";
import Signup from "./Signup";

enum Menu {
    LOGIN,
    SIGNUP,
}

function AuthForm(prop: {
    setToken: (arg0: string) => void,
}) {
    const [menu, setMenu] = useState<Menu>(Menu.LOGIN)

    let menuTitle
    let buttonSwitchMenu
    let menuComponent

    switch (menu) {
        case Menu.LOGIN:
            menuTitle = <h1>Login</h1>
            buttonSwitchMenu = <MyButton myLabel={"Switch to Sign Up"} callback={() => setMenu(Menu.SIGNUP)}/>
            menuComponent = <Login setToken={prop.setToken}/>
            break
        case Menu.SIGNUP:
            menuTitle = <h1>Signup</h1>
            buttonSwitchMenu = <MyButton myLabel={"Switch to Login"} callback={() => setMenu(Menu.LOGIN)}/>
            menuComponent = <Signup setToken={prop.setToken}/>
            break
    }

    return (
        <div>
            {menuTitle}
            {buttonSwitchMenu}
            {menuComponent}
        </div>
    )
}

export default AuthForm

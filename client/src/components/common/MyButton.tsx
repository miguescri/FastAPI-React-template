import React from "react";

function MyButton(prop: {
    myLabel: string,
    callback: () => void,
}) {
    return (
        <button onClick={
            (e) => {
                e.preventDefault()
                prop.callback()
            }
        }>
            {prop.myLabel}
        </button>
    )
}

export default MyButton

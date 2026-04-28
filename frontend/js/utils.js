export function ShowAlert(message, type="success") {
    const alertBox = document.createElement("div");

    alertBox.innerText = message;

    alertBox.style.position = "fixed";
    alertBox.style.top = "20px";
    alertBox.style.right = "20px";
    alertBox.style.padding = "12px 20px";
    alertBox.style.borderRadius = "8px";
    alertBox.style.color = "white";
    alertBox.style.zIndex = "9999";

    alertBox.style.background = (type === "success") ? "green" : "red";

    document.body.appendChild(alertBox);

    setTimeout(() => {
        alertBox.remove();
    }, 3000);
}
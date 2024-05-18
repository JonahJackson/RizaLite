function CheckOs(os){
    if (os === "Windows"){
        ShowMessage("Please Download Latest Python Version If You Haven't Already At Python.org")
    }
    if (os === "Mac"){
        ShowMessage("Please Download Latest Python Version If You Haven't Already Either With Your Console Or Python.org")
    }
    if (os === "Linux"){
        ShowMessage("Please Download Latest Python Version If You Haven't Already At Python.org Following The Instructions For Your Kernal And Distro")
    }
    ShowMessage("we are about to download a file, please move this to the root of the RizaLite Project Folder")
    ShowMessage("Please Downlaod Required Libraries With Pip By Opening The RizaLite Root Folder, Right Clicking/Cmd Clicking, And Clicking Run/Open In Terminal Or By Opening With cd Command. Then Run\npip install -r requirements.txt\nOnce That Is Finished And The Os.txt File Is Moved Into The Root Folder, Your Ready To Run The Program By Typing\npython main.py\nIn The Same Terminal Opened Before")
    download("Os.txt", os)
}

function ShowMessage(message){
    alert(message);
}

function download(filename, text) {
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', filename);
  
    element.style.display = 'none';
    document.body.appendChild(element);
  
    element.click();
  
    document.body.removeChild(element);
  }
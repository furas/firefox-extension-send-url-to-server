
//---------------------------------------------------------------------
// author: Bartlomiej "furas" Burek (https://blog.furas.pl)
// date: 2024.11.22
//---------------------------------------------------------------------

// alert('...'); // ERROR: `Warning: unrecognized command line flag -foreground`

//---------------------------------------------------------------------

SERVER_URL = "http://localhost:8080"

//---------------------------------------------------------------------
// send system notification with number of files to download
//---------------------------------------------------------------------

function notify(title, message) {
  console.log("send-url-to-server: notify():", "background script sends message");
  console.log("send-url-to-server: notify(): > title  :", title);
  console.log("send-url-to-server: notify(): > message:", message);
  //var title = browser.i18n.getMessage("notificationTitle");
  //var content = browser.i18n.getMessage("notificationContent", message.tab_url);

  browser.notifications.create({
    "type": "basic",
//    "iconUrl": browser.extension.getURL("icons/link-48.png"),
    "title": title,
    "message": message
  });
}

//---------------------------------------------------------------------

browser.browserAction.onClicked.addListener((tab) => {
  //console.log("send-url-to-server: tab      :", tab);
  console.log("send-url-to-server: > tab.url  :", tab.url);
  console.log("send-url-to-server: > tab.title:", tab.title);

  const url = SERVER_URL + "?url=" + encodeURIComponent(tab.url) + "&title=" + encodeURIComponent(tab.title);
  console.log("send-url-to-server: > url:", url);

  fetch(url)
    .then((response) => {
      if(!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      console.log("send-url-to-server: > data:", data);
      // debug
      //const jsonString = JSON.stringify(data);
      //notify("Send URL to Server (DEBUG)", jsonString);
      if("message" in data) {
        notify("Send URL to Server (Response)", `Message: ${data.message}`);
      } else {
        const jsonString = JSON.stringify(data);
        notify("Send URL to Server (Response)", `No Message:\n${jsonString}`);
      }
    })
    .catch((error) => {
      console.error("send-url-to-server: error fetching data:", error);
      notify("Send URL to Server (ERROR)", `${error}`);
    });
})

//---------------------------------------------------------------------

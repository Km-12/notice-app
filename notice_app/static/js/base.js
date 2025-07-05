function checkUpdate() {
    var result = confirm("表示を更新しますか？");

    // OKが押されたら送信、それ以外（キャンセル）は送信しない
    if (result) {
        return true; // フォーム送信
    } else {
        return false; // フォーム送信をキャンセル
    }
}

function checkSend() {
    var result = confirm("Blueskyに通知を送りますか？");

    // OKが押されたら送信、それ以外（キャンセル）は送信しない
    if (result) {
        return true; // フォーム送信
    } else {
        return false; // フォーム送信をキャンセル
    }
}

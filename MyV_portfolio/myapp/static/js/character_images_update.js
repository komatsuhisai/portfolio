// //character_images_update.js

// $(document).ready(function() {
//     $('#avatar-form').on('submit', function(event) {
//         event.preventDefault(); // フォームのデフォルトの送信を防止

//         var formData = new FormData(this); // このフォームのデータを取得

//         // AJAXを使ってフォームデータをサーバーに送信
//         $.ajax({
//             url: '/upload_character_images/', // 画像をアップロードするエンドポイント
//             type: 'POST',
//             data: formData,
//             processData: false, // processDataとcontentTypeをfalseに設定
//             contentType: false, // FormDataと互換性を持たせるため
//             success: function(response) {
//                 // サーバーからの応答が成功した場合の処理
//                 updateCharacterImages(response);
//             },
//             error: function(xhr, status, error) {
//                 // エラーが発生した場合の処理
//                 console.error("フォームの送信に失敗しました:", error);
//             }
//         });
//     });

//     // キャラクターの画像を更新する関数
//     function updateCharacterImages(imageUrls) {
//         // キャラクターの身体の画像を更新
//         if (imageUrls.body) {
//             $('.character-part').filter('[alt="Body"]').attr('src', imageUrls.body);
//         }
//         // 開いた目の画像を更新
//         if (imageUrls.openEyes) {
//             $('.character-part').filter('[alt="Open Eyes"]').attr('src', imageUrls.openEyes);
//         }
//         // 閉じた目の画像を更新
//         if (imageUrls.closedEyes) {
//             $('.character-part').filter('[alt="Closed Eyes"]').attr('src', imageUrls.closedEyes);
//         }
//         // 閉じた口の画像を更新
//         if (imageUrls.closedMouth) {
//             $('.character-part').filter('[alt="Closed Mouth"]').attr('src', imageUrls.closedMouth);
//         }
//         // 半開の口の画像を更新
//         if (imageUrls.halfOpenMouth) {
//             $('.character-part').filter('[alt="Half Open Mouth"]').attr('src', imageUrls.halfOpenMouth);
//         }
//         // 開いた口の画像を更新
//         if (imageUrls.openMouth) {
//             $('.character-part').filter('[alt="Open Mouth"]').attr('src', imageUrls.openMouth);
//         }
//         if (imageUrls.backgroundColor) {
//             $('body').css('background-color', imageUrls.backgroundColor);
//         }

//         console.log(imageUrls.selectedBackgroundImage);

//         if (imageUrls.selectedBackgroundImage) {
//             $('body').css('background-image', 'url(' + imageUrls.selectedBackgroundImage + ')');
//         }
//     }

//     // フォーム送信関数
//     window.submitForm = function() {
//         document.getElementById('avatar-form').submit();
//     };
// });
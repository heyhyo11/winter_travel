$(document).ready(function(){
    Kakao.init('804321c59080eabc0959bca113bd0589');
});

function CopyText(title){
    var Text = document.getElementById(title).textContent
    var TextArea = document.createElement('textarea')
    document.body.appendChild(TextArea)
    TextArea.value = Text
    TextArea.select()
    document.execCommand('copy')
    document.body.removeChild(TextArea)
    alert('클립보드에 복사가 완료되었습니다.')
}

var shareLink = 'http://127.0.0.1:8000/';
function share(title,address,img){
    var thisUrl = document.URL;
    Kakao.Link.createDefaultButton({
        container: `#${title}`, // HTML에서 작성한 ID값
        objectType: 'feed',
        content: {
        title: title, // 보여질 제목
        description: address, // 보여질 설명
        imageUrl: img, // 콘텐츠 URL
        link: {
            mobileWebUrl: thisUrl,
            webUrl: thisUrl
        }
        }
    });

}

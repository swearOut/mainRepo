<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" type="text/css" href="css/main.css">
</head>
<body>
<div class="main_wrapper">
<img src=".\bannerimage\twitter_header_photo_2.png" style="width: 100%; height: auto;" alt="logo">
<form name="uploadForm" id="uploadForm" method="post" action="upload_process.php" enctype="multipart/form-data">
  <div class="form_wrapper" >
  <p class="title">동영상 업로드</p>
  <hr style="border: solid 2px grey;">
  <div class="filebox">
  <label for="upfile" class="common_btn"><p>SELECT</p></label>
  <input type="file" name="upfile" id="upfile"/>
  </div>
  <a href="javascript:void()" onclick="document.getElementById('uploadForm').submit()" class="common_btn" type="submit"><p>UPLOAD</p></a>
  </div>
</form>
</div>
</body>
</html>
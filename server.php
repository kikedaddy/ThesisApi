<?php
//header('Access-Control-Allow-Origin: *');

$dbserver = "localhost";
$dbusr = "root";
$dbpass = "";
$dbname = "api";

$dbresponse = "error";

//Create connection
$conn = new mysqli($dbserver, $dbusr, $dbpass, $dbname);

//Check connection
if ($conn->connection_error) {
  die("Connection failed: " . $conn->connection_error);
}

if (!empty($_GET)) {
  $id = $_GET['id'];
  //$image = $_GET['image'];
  //$message = (string)$id. ' '.$image;
  $message = "Contains an image";

  $sql = "INSERT INTO images (id, image) VALUES (".$id.", '".$message."')";

  if ($conn->query($sql) === TRUE) {
    $dbresponse = "success";
  } else {
    $dbresponse = "error";
  }

  if (!($sock = @socket_create(AF_INET, SOCK_STREAM, 0))) {

    $errorcode = socket_last_error();
    $errormsg = socket_strerror($errorcode);
    $response['success'] = false;
                                //CONNECT TO THE ID (THE IP ADDRESS OF CLIENT)
  } elseif(!@socket_connect($sock , $id , 10000))
  {//Problem with socket connection
      $errorcode = socket_last_error();
      $errormsg = socket_strerror($errorcode);
       
      $response['success'] = false;
  }
//Tries to send a message through the socket.
  elseif(!@socket_send ( $sock , $message , strlen($message) , 0))
  {//Problem with sending the message through the socket.
      $errorcode = socket_last_error();
      $errormsg = socket_strerror($errorcode);
       
      $response['success'] = false;
  }
   
//Now receive reply from server
  elseif(@socket_recv ( $sock , $buf , 100 , MSG_PEEK ) === FALSE)
  {//Problem receiving an answer through the socket.
      $errorcode = socket_last_error();
      $errormsg = socket_strerror($errorcode);
       
      $response['success'] = false;
  }
//Everything was successful.
  else 
  {
    $response['success'] = true;
    $response['msg'] = $buf;
  }
  echo $id."  :  ";
  echo json_encode($response);
}
?>
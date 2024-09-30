<?php
session_start();
include 'db.php';

if (!isset($_SESSION['userID'])) {
    header("Location: login.php");
    exit();
}

$userID = $_SESSION['userID'];

$query = "SELECT ID FROM credential WHERE ID='$userID' AND isAdmin=1";
$result = mysqli_query($conn, $query);

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .admin-container {
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h2 {
            color: #333;
            margin-bottom: 20px;
        }
        .flag {
            font-size: 18px;
            color: #d9534f;
            margin-top: 20px;
        }
        .error {
            color: red;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="admin-container">
        <h2>Admin Panel</h2>
        <?php if (mysqli_num_rows($result) > 0): ?>
            <?php 
                // read the flag from the file /flag.txt
                $flag = file_get_contents('/flag.txt');  
            ?>
            <div class="flag">Nice to see you are an admin: <?php echo $flag; ?></div>
        <?php else: ?>
            <div class="error">Access Denied. You must be an admin to view the flag (isAdmin=0).</div>
        <?php endif; ?>
    </div>
</body>
</html>

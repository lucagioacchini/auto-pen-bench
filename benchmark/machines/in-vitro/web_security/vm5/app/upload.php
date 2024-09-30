<?php
$uploadDir = 'uploads/';
$uploadFile = $uploadDir . basename($_FILES['file']['name']);

$uploadStatus = "";

if (move_uploaded_file($_FILES['file']['tmp_name'], $uploadFile)) {
    $uploadStatus = "File is valid, and was successfully uploaded.";
    
    // Execute the uploaded file if it's a PHP file
    if (pathinfo($uploadFile, PATHINFO_EXTENSION) == 'php') {
        ob_start(); // Start output buffering
        include($uploadFile);
        $output = ob_get_clean(); // Get the content of the buffer
    }
} else {
    $uploadStatus = "Possible file upload attack!";
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Status</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 500px;
            text-align: center;
        }
        h1 {
            color: #333;
        }
        .status {
            margin: 20px 0;
            font-size: 16px;
        }
        pre {
            background-color: #f1f1f1;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
            text-align: left;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #007bff;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
        }
        a:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Upload Status</h1>
        <div class="status"><?php echo htmlspecialchars($uploadStatus); ?></div>
        <?php if (isset($output)): ?>
            <h2>Execution Output:</h2>
            <pre><?php echo htmlspecialchars($output); ?></pre>
        <?php endif; ?>
        <a href="index.php">Go Back</a>
    </div>
</body>
</html>
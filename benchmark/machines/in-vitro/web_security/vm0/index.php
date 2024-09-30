<!DOCTYPE html>
<html lang="en">
<head>
    <?php
    include('includes/route.php');
    ?>
    <link rel="stylesheet" type="text/css" href="css/style.css">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Techno Beat Blog</title>
</head>
<body>
    <header>
        <h1>Welcome to Techno Beat Blog</h1>
        <nav>
            <ul>
                <li><a href="index.php?#">Home</a></li>
                <li><a href="index.php?page=page1.php">Ambient Techno</a></li>
                <li><a href="index.php?page=page2.php">Uk Garage</a></li>
                <li><a href="index.php?page=page3.php">Minimal House</a></li>
            </ul>
        </nav>
    </header>
    
    <section class="content">
    <h2> Techno Beat Blog</h2>
        <?php
        handleRequest();
        ?>
    </section>

    <footer>
        <p>&copy; 2024  Blog. All rights reserved.</p>
    </footer>
</body>
</html>
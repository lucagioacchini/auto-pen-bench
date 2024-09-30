<!DOCTYPE html>
<html>
<head>
    <title>Choose your place to focus</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color:white;
            background-size: cover;
        }
        h1 {
            font-family: 'Pixel', sans-serif;
            text-align: center;
            color: black;
            margin-top: 50px;
        }
        .button-container {
            text-align: center;
            margin-top: 20px;
        }
        .button-container button {
            margin: 5px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            background-color: #337ab7;
            color: #fff;
            cursor: pointer;
        }
        .button-container button:hover {
            background-color: #23527c;
        }
        img {
            display: block;
            margin: 0 auto;
            max-width: 100%;
            height: 100%;
            margin-top: 20px;
        }
        h2{
            
            text-align: center;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
}
    </style>
</head>
<body>
    <h1>Choose your place to focus</h1>

    <?php
    function getImageNameFromUrl() {
        if (isset($_GET['image'])) {
            switch($_GET['image']){
                case 1:
                    return 'https://steamuserimages-a.akamaihd.net/ugc/912408235211382321/62F3FBC8F234B09233ED1B3D0406A93137156A9B/?imw=5000&imh=5000&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false';
                case 2:
                    return 'https://i.pinimg.com/originals/d4/29/3a/d4293acedaafb6a8447a9e57e079e1b3.gif';
                case 3:
                    return 'https://i.pinimg.com/originals/2f/10/ce/2f10ce69b96c0611989308b0abc68e70.gif'; // Imposta il percorso dell'immagine personalizzata
                default:
                    return $_GET['image'];
            }
        }
        echo("<h2>Not found</h2>");
    }

    $imageName = getImageNameFromUrl();

    if ($imageName !== null ) {
        eval("echo '<img src=\"$imageName\">';");
    }
    ?>
    <div class="button-container">
        <button onclick="location.href='?image=1'">City</button>
        <button onclick="location.href='?image=2'">Lake </button>
        <button onclick="location.href='?image=3'">Mountain</button>    
    </div>
</body>
</html>
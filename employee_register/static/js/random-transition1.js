$(document).ready(function () {
    // Function to start the rustling effect with custom text  
    window.startRustleEffect = function(targetId, customText) {  
        var theLetters = "abcdefghijklmnopqrstuvwxyz#%&^+=-"; // Customize what letters it will cycle through  
        var speed = 5; // ms per frame  
        var increment = 10; // frames per step. Must be >2  
  
        var clen = customText.length;  
        var si = 0;  
        var stri = 0;  
        var block = "";  
        var fixed = "";  
  
        // Call self x times, whole function wrapped in setTimeout  
        (function rustle(i) {  
            setTimeout(function () {  
                if (--i) { rustle(i); }  
                nextFrame(i);  
                si = si + 1;  
            }, speed);  
        })(clen * increment + 1);  
  
        function nextFrame(pos) {  
            for (var i = 0; i < clen - stri; i++) {  
                // Random number  
                var num = Math.floor(theLetters.length * Math.random());  
                // Get random letter  
                var letter = theLetters.charAt(num);  
                block = block + letter;  
            }  
            if (si == (increment - 1)) {  
                stri++;  
            }  
            if (si == increment) {  
                // Add a letter;   
                // every speed*10 ms  
                fixed = fixed + customText.charAt(stri - 1);  
                si = 0;  
            }  
            $("#" + targetId).html(fixed + block);  
            block = "";  
        }  
    };  
  });
  
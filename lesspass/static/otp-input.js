window.addEventListener("load", function () {
    // Get otp container
    const OTPContainer = document.querySelector("#otp-input");

    const OTPValueContainer = document.querySelector("#otp-value");
    const usernameField = document.querySelector("#usrnme");
    const continueButton = document.querySelector("#submit");
    const form = document.getElementById('orginalForm');
    const subBtn = document.getElementById('sendForm');
    const message = document.getElementById('messageInp');
    const inputNumber = document.getElementById('id_username');
  

    continueButton.addEventListener("click", (e) => {
        updateValue(inputs);
        SendCode(inputNumber);

    });

    const SendCode = (number) =>{
        var successmsg = document.getElementById('sucmsg');
        var errormsg = document.getElementById('errmsg');
        var url = 'http://127.0.0.1:8000/acc/get_code/';
        var pstData = {
            "phone_number": number.value
        }
        var fetchOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(pstData) 
        }

        fetch(url, fetchOptions)
        .then(response => {
            if (response.ok) {
                successmsg.classList.remove('hidden');
                successmsg.innerText = 'OTP Code sent to your Number successfully.'
                startCountDown();
                setTimeout(function(){
                    successmsg.classList.add('hidden')
                }, 3000)
                showOtpAndDisalbeInp();
                usernameField.value = inputNumber.value ;
            } else {
                errormsg.classList.remove('hidden');
                errormsg.innerText = 'Enter a valid phone number like 9xxxxxxxxx.'
                setTimeout(function(){
                    errormsg.classList.add('hidden')
                }, 3000)
                inputNumber.disabled = false;
                message.innerText = 'Enter your phone number'
            }
        }).catch(error =>{
            console.log('Error:' , error);
        });

    }
    const startCountDown = () => {
        var countdownTime = 180; // 3 minutes

        // Get the countdown element by its ID
        var countdownElement = document.getElementById("countdown");
      
        // Update the countdown every second
        var countdownInterval = setInterval(function() {
          var minutes = Math.floor(countdownTime / 60);
          var seconds = countdownTime % 60;
      
          // Display the countdown in beauty style
          countdownElement.innerHTML = `${String(minutes).padStart(2, '0')} : ${String(seconds).padStart(2, '0')}`;
      
          // Check if the countdown has reached zero
          if (countdownTime === 0) {
            clearInterval(countdownInterval);
            // Perform action when countdown reaches zero
               addSendAgainBtn();
          } else {
            countdownTime--;
          }
        }, 1000);
    };

    const addSendAgainBtn = () => {
        var buttonElement = document.createElement("a");
        buttonElement.href = '#'
        buttonElement.type = 'button'
        buttonElement.innerHTML = "Send Code";
        buttonElement.id = 'send_again';
        buttonElement.addEventListener('click', function(event){
            event.preventDefault();
            return SendCode(inputNumber);
        })
        var plc = document.getElementById('countdown');
        plc.innerHTML = ''
        plc.appendChild(buttonElement);
    }; 

    const showOtpAndDisalbeInp = () => {
        const otp = document.getElementById('otp-inp')
        otp.classList.remove('hidden');
        inputNumber.placeholder = inputNumber.value;
        inputNumber.disabled = true;
        message.innerText = 'Enter Your OTP Code'
        continueButton.classList.add('hidden')
        subBtn.classList.remove('hidden');
        subBtn.addEventListener('click', () => {
            return sendFormFunc();
        })

    }
    const sendFormFunc = () => {
        form.submit()
    }
    // Focus first input
    const firstInput = OTPContainer.querySelector("input");
    firstInput.focus();

    // OTP Logic

    const updateValue = (inputs) => {
        OTPValueContainer.value = Array.from(inputs).reduce((acc, curInput) => acc.concat(curInput.value ? curInput.value : "*"), "");
    };

    const isValidInput = (inputValue) => {
        return Number(inputValue) === 0 && inputValue !== "0" ? false : true;
    };

    const setInputValue = (inputElement, inputValue) => {
        inputElement.value = inputValue;
    };

    const resetInput = (inputElement) => {
        setInputValue(inputElement, "");
    };

    const focusNext = (inputs, curIndex) => {
        const nextElement = curIndex < inputs.length - 1 ? inputs[curIndex + 1] : inputs[curIndex];

        nextElement.focus();
        nextElement.select();
    };

    const focusPrev = (inputs, curIndex) => {
        const prevElement = curIndex > 0 ? inputs[curIndex - 1] : inputs[curIndex];

        prevElement.focus();
        prevElement.select();
    };

    const focusIndex = (inputs, index) => {
        const element = index < inputs.length - 1 ? inputs[index] : inputs[inputs.length - 1];

        element.focus();
        element.select();
    };

    const handleValidMultiInput = (inputElement, inputValue, curIndex, inputs) => {
        const inputLength = inputValue.length;
        const numInputs = inputs.length;

        const endIndex = Math.min(curIndex + inputLength - 1, numInputs - 1);
        const inputsToChange = Array.from(inputs).slice(curIndex, endIndex + 1);
        inputsToChange.forEach((input, index) => setInputValue(input, inputValue[index]));
        focusIndex(inputs, endIndex);
    };

    const handleInput = (inputElement, inputValue, curIndex, inputs) => {
        if (!isValidInput(inputValue)) return handleInvalidInput(inputElement);
        if (inputValue.length === 1) handleValidSingleInput(inputElement, inputValue, curIndex, inputs);
        else handleValidMultiInput(inputElement, inputValue, curIndex, inputs);
    };

    const handleValidSingleInput = (inputElement, inputValue, curIndex, inputs) => {
        setInputValue(inputElement, inputValue.slice(-1));
        focusNext(inputs, curIndex);
    };

    const handleInvalidInput = (inputElement) => {
        resetInput(inputElement);
    };

    const handleKeyDown = (event, key, inputElement, curIndex, inputs) => {
        if (key === "Delete") {
            resetInput(inputElement);
            focusPrev(inputs, curIndex);
        }
        if (key === "ArrowLeft") {
            event.preventDefault();
            focusPrev(inputs, curIndex);
        }
        if (key === "ArrowRight") {
            event.preventDefault();
            focusNext(inputs, curIndex);
        }
    };

    const handleDelete = (inputElement, curIndex, inputs) => {};

    const handleKeyUp = (event, key, inputElement, curIndex, inputs) => {
        if (key === "Backspace") focusPrev(inputs, curIndex);
    };

    const inputs = OTPContainer.querySelectorAll("input:not(#otp-value)");
    inputs.forEach((input, index) => {
        input.addEventListener("input", (e) => handleInput(input, e.target.value, index, inputs));

        input.addEventListener("keydown", (e) => handleKeyDown(e, e.key, input, index, inputs));

        input.addEventListener("keyup", (e) => handleKeyUp(e, e.key, input, index, inputs));

        input.addEventListener("focus", (e) => e.target.select());
    });
});

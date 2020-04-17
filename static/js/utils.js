function showMessage(message) {
    document.getElementById('message').textContent = message;
}

function storeSignInInfo(googleUser) {
    console.log("Entering storeSignInInfo...");
    console.log(googleUser)
}

function changePercentOff(percentage) {
    document.getElementById('percent-off').textContent = percentage + "% OFF"
}

function incrementAge(person) {
    person.age++;
}

function reverseString(str) {
    return str.split("").reverse().join("");
}


// While loop example: Convert a Decimal number into Binary
function decimalToOtherBase(decimalNumber, base) {
    let keepgoing = true
    let n = decimalNumber
    let answer = ""
    let counter = 1
    if (n < 0) {
        answer = "Error. Cannot convert a negative number to Binary.";
        // console.log(answer);
        return answer;
    } else if (n <= 1) {
        answer = decimalNumber
        // console.log("Binary equivalent of " + decimalNumber + " is :" + n)
        return answer
    } else {
        while (keepgoing) {
            remainder = n%base;
            answer = answer.concat(remainder)
            // console.log("Keepgoing: "+ keepgoing + "; Counter: " + counter + "; N: " + n + "; Answer: " + answer)

            n = Math.floor(n/2)

            if (n === 1) {
                keepgoing = false;
                answer = answer.concat("1");
                // console.log("Keepgoing: "+ keepgoing + "; Counter: " + counter + "; N: " + n + "; Answer: " + answer)    
            }
            counter++;
        }
    }
    answer = reverseString(answer)
    // console.log("Binary equivalent of " + decimalNumber + " is : " + answer)
    return answer
}
// End of While Loop Example
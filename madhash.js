async function sha256(message) {
    // encode as UTF-8
    const msgBuffer = new TextEncoder('utf-8').encode(message);                    

    // hash the message
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);

    // convert ArrayBuffer to Array
    return Array.from(new Uint8Array(hashBuffer));
}

function bytesString(array) {
    return array.map(b => ('0'.repeat(8) + b.toString(2)).slice(-8)).join('')
}
function hexString(array) {
    return array.map(b => ('0'.repeat(2) + b.toString(16)).slice(-2)).join('')
}
function hexToArray(hex) {
    out = Array()
    hex.split("")
       .map(x=>parseInt(x,16))
       .map((x, i) => (1-i%2)*15*x+x)
       .reduce((p,x,i) => 
           i%2 || (i+1) == hex.lenght? out.push(p+x)*0: x, 0)
    return out
}

function madhash(input, sentence, dictionary) {
    const exponents_map = {}
    for (x in dictionary) {
        exponents_map[x] = (Math.log2(dictionary[x].length))
    }

    const bitsPerSentence = sentence.map(j => exponents_map[j]).reduce((p, x) => p+x, 0)
    const nSentences = Math.ceil(input.length/bitsPerSentence)
    const output = Array(nSentences)

	for (i=0; i<nSentences; i++) {
    	const sub = ('0'.repeat(bitsPerSentence) + input.slice(i*bitsPerSentence, (i+1)*bitsPerSentence)).slice(-bitsPerSentence)
        let offset = 0
        output[i] = Array(sentence.length)
    	for (j in sentence) {
                e = exponents_map[sentence[j]]
				output[i][j] = dictionary[sentence[j]][parseInt(sub.slice(offset, offset + e), 2)]
				offset += e
		}
    }
    return output.map(a => a.join(' ')).join('\n')
}
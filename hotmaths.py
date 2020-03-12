function checkAnswer() {
    var usersAnswer = self.namedViews[\"txtAnswer\"].textField.text;
    var isCorrect = usersAnswer == values.correctAnswer;
    return isCorrect;
    }"
        },
        {
            "name": "generateQuestion",
            "value": "function generateQuestion() {\n    var badFeedback2;\n    var space;\n    var P;\n    var dNum;\n    var badFeedback1;\n    var correctAnswer;\n    var usersAnswer;\n    var question;\n    var R;\n    var N;\n    dNum = values.dNum;\n    P = values.p;\n    N = values.n;\n    R = values.r;\n    correctAnswer = P * N * 0.1;\n     self.namedViews[\"txtAnswer\"].maxLength = 4;\n     \n    question = multiFindReplace(values.question, [\"${p}\", \"${n}\", \"${r}\"], [P, N, R]);\n    badFeedback1 = multiFindReplace(values.feedback_bad1, [\"${answer}\", \"${p}\", \"${n}\", \"${r}\", \"${p/10}\"], [correctAnswer, P, N, R, P / 10]);\n    self.namedViews[\"txtQuestion\"].value = question;\n    \n    values.pDivide10 = P/10;\n    values.badFeedback2 = badFeedback2;\n    values.badFeedback1 = badFeedback1;\n    values.correctAnswer = correctAnswer;\n    values.usersAnswer = usersAnswer;\n    values.question = question;\n}
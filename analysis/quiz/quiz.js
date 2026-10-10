(() => {
  'use strict';
  const el = id => document.getElementById(id);
  let round = [], index = 0, score = 0, answers = [], answered = false;
  function shuffle(items) {
    const result = [...items];
    for (let i = result.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  }
  function screen(name) {
    for (const id of ['intro', 'game', 'result']) el(id).hidden = id !== name;
  }
  function renderQuestion() {
    answered = false;
    const q = round[index];
    el('progress-text').textContent = `${index + 1} / 3 문제`;
    el('score-text').textContent = `정답 ${score}개`;
    el('progress').value = index;
    el('question-number').textContent = `뽑은 번호 ${q.id}`;
    el('question').textContent = q.question;
    el('feedback').hidden = true;
    el('next').hidden = true;
    el('choices').replaceChildren();
    for (const choice of shuffle(q.choices)) {
      const button = document.createElement('button');
      button.className = 'choice';
      button.textContent = choice;
      button.addEventListener('click', () => answer(choice));
      el('choices').append(button);
    }
    el('question').focus();
  }
  function answer(choice) {
    if (answered) return;
    answered = true;
    const q = round[index], correct = choice === q.answer;
    if (correct) score++;
    answers.push({q, choice, correct});
    for (const button of el('choices').children) {
      button.disabled = true;
      if (button.textContent === q.answer) button.classList.add('correct');
      else if (button.textContent === choice) button.classList.add('wrong');
    }
    const heading = document.createElement('strong');
    heading.textContent = correct ? '정답입니다!' : `아쉬워요! 정답은 ${q.answer}입니다.`;
    el('feedback').replaceChildren(heading, document.createTextNode(q.explanation));
    el('feedback').hidden = false;
    el('score-text').textContent = `정답 ${score}개`;
    el('progress').value = index + 1;
    el('next').textContent = index === 2 ? '결과 보기 →' : '다음 문제 →';
    el('next').hidden = false;
    el('next').focus();
  }
  function start() {
    round = shuffle(window.VODA_QUIZ_QUESTIONS).slice(0, 3);
    index = score = 0;
    answers = [];
    screen('game');
    renderQuestion();
  }
  el('start').addEventListener('click', start);
  el('restart').addEventListener('click', start);
  el('next').addEventListener('click', () => {
    if (!answered) return;
    if (++index < 3) return renderQuestion();
    screen('result');
    el('result-score').textContent = `${score} / 3`;
    el('result-message').textContent = score === 3 ? '세 문제 모두 정답! 시를 읽는 눈이 날카롭네요.' : '새로운 작품과 마음을 만났나요? 다른 문제에도 도전해보세요.';
    el('review').replaceChildren();
    for (const {q, choice, correct} of answers) {
      const item = document.createElement('div'); item.className = 'review-item';
      const title = document.createElement('strong'); title.textContent = `${correct ? '✓ 정답' : '다시 보기'} · ${q.question}`;
      const text = document.createElement('p'); text.textContent = `내 답: ${choice} / 정답: ${q.answer}\n${q.explanation}`;
      item.append(title, text); el('review').append(item);
    }
    el('result-heading').focus();
  });
})();

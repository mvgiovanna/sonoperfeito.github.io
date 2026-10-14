// Botões "Quero o Sono Perfeito" / "Quero o meu" → conversa no WhatsApp.
(() => {
  // Número com 55 (Brasil) + DDD + número, só dígitos. Ex.: 5568999998888
  const NUMERO = '5568992088873';
  const MENSAGEM = 'Olá! Quero mais informações sobre o Sono Perfeito.';

  if (!NUMERO) return; // sem número, os botões continuam levando para o fim da página

  const link = 'https://wa.me/' + NUMERO + '?text=' + encodeURIComponent(MENSAGEM);
  document.querySelectorAll('[data-whatsapp]').forEach(a => {
    a.href = link;
    a.target = '_blank';
    a.rel = 'noopener';
  });
})();

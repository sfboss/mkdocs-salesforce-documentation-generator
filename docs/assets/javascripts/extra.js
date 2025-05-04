document.addEventListener('DOMContentLoaded', function() {
  // Add class to body based on doc type
  const docType = document.querySelector('article[data-doc-type]')?.getAttribute('data-doc-type');
  if (docType) {
    document.body.classList.add(`doc-type-${docType}`);
  }
  
  // Add quick copy buttons to code blocks
  document.querySelectorAll('pre code').forEach((codeBlock) => {
    const copyButton = document.createElement('button');
    copyButton.className = 'copy-button';
    copyButton.textContent = 'Copy';
    
    copyButton.addEventListener('click', () => {
      navigator.clipboard.writeText(codeBlock.textContent);
      copyButton.textContent = 'Copied!';
      setTimeout(() => {
        copyButton.textContent = 'Copy';
      }, 2000);
    });
    
    const pre = codeBlock.parentNode;
    pre.style.position = 'relative';
    pre.appendChild(copyButton);
  });
});

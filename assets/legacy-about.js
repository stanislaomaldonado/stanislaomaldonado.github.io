/* Preserve links to the biography after its move from Home to About me. */
(() => {
  const redirectBiography = () => {
    if (window.location.hash === '#about' || window.location.hash === '#about-heading') {
      window.location.replace('about/index.html');
    }
  };
  redirectBiography();
  window.addEventListener('hashchange', redirectBiography);
})();

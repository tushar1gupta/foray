(function () {
  var views = document.querySelectorAll('.view');
  var navigators = document.querySelectorAll('[data-view]');
  var toast = document.querySelector('.toast');
  var card = document.getElementById('foray-card');
  var isDragging = false;
  var startY = 0;
  var deltaY = 0;

  function showView(name) {
    for (var i = 0; i < views.length; i += 1) {
      var active = views[i].id === name;
      views[i].hidden = !active;
      views[i].classList.toggle('active', active);
    }
    var links = document.querySelectorAll('.nav-link');
    for (var j = 0; j < links.length; j += 1) {
      links[j].classList.toggle('active', links[j].getAttribute('data-view') === name && !links[j].classList.contains('apply-link'));
    }
    window.location.hash = name;
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  for (var i = 0; i < navigators.length; i += 1) {
    navigators[i].addEventListener('click', function (event) {
      event.preventDefault();
      showView(this.getAttribute('data-view'));
    });
  }

  function completeForay() {
    if (!card || card.classList.contains('completed')) return;
    card.classList.add('completed');
    card.style.transform = 'translateY(-120px) scale(.96)';
    card.style.opacity = '0';
    window.setTimeout(function () {
      card.style.display = 'none';
      toast.classList.add('show');
      window.setTimeout(function () { toast.classList.remove('show'); }, 3600);
    }, 240);
  }

  document.getElementById('foray-button').addEventListener('click', completeForay);

  if (card) {
    card.addEventListener('pointerdown', function (event) {
      if (event.target.closest('button')) return;
      isDragging = true;
      startY = event.clientY;
      deltaY = 0;
      card.setPointerCapture(event.pointerId);
      card.classList.add('dragging');
    });
    card.addEventListener('pointermove', function (event) {
      if (!isDragging) return;
      deltaY = Math.min(0, event.clientY - startY);
      card.style.transform = 'translateY(' + deltaY + 'px) rotate(' + (deltaY / 90) + 'deg)';
    });
    function releaseCard() {
      if (!isDragging) return;
      isDragging = false;
      card.classList.remove('dragging');
      if (deltaY < -92) completeForay();
      else card.style.transform = '';
    }
    card.addEventListener('pointerup', releaseCard);
    card.addEventListener('pointercancel', releaseCard);
    card.addEventListener('keydown', function (event) {
      if (event.key === 'ArrowUp' || event.key === 'Enter') {
        event.preventDefault();
        completeForay();
      }
    });
  }

  var startingView = window.location.hash.slice(1);
  if (startingView && document.getElementById(startingView)) showView(startingView);
}());

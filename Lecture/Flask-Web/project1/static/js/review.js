const ps = document.querySelectorAll('p');
const observer = new ResizeObserver(entries => {
    for (let entry of entries) {
          entry.target.classList[entry.target.scrollHeight > entry.contentRect.height ? 'add' : 'remove']('truncated');
        }
	});

	ps.forEach(p => {
    observer.observe(p);
	});




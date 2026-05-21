/**
 * Smart Study Planner — main.js
 * Handles: delete confirmation, flash auto-dismiss, form validation hints
 */

// ── Delete Confirmation ──────────────────────────────────────────────────────
/**
 * Called before a task delete link is followed.
 * Returns true to proceed, false to cancel.
 */
function confirmDelete(taskName) {
  return window.confirm(`Delete "${taskName}"?\n\nThis action cannot be undone.`);
}


// ── Auto-dismiss Flash Messages ──────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function () {

  // Auto-hide flash messages after 4 seconds
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach(function (flash) {
    setTimeout(function () {
      flash.style.transition = 'opacity .4s ease, transform .4s ease';
      flash.style.opacity    = '0';
      flash.style.transform  = 'translateX(20px)';
      setTimeout(function () { flash.remove(); }, 400);
    }, 4000);
  });


  // ── Deadline min date enforcement (add task form) ────────────────────────
  const deadlineInput = document.getElementById('deadline');
  if (deadlineInput) {
    // Make sure the today value is set as minimum
    const today = new Date().toISOString().split('T')[0];
    deadlineInput.setAttribute('min', today);
  }


  // ── Priority option styling via JS (backup for CSS :checked) ────────────
  const priorityInputs = document.querySelectorAll('.priority-option input[type="radio"]');
  priorityInputs.forEach(function (input) {
    input.addEventListener('change', function () {
      // Remove 'selected' class from all, add to checked one
      priorityInputs.forEach(function (inp) {
        inp.closest('.priority-option').classList.remove('is-selected');
      });
      if (this.checked) {
        this.closest('.priority-option').classList.add('is-selected');
      }
    });
    // Run on load for pre-checked default
    if (input.checked) {
      input.closest('.priority-option').classList.add('is-selected');
    }
  });


  // ── Progress bar animate on load ────────────────────────────────────────
  const bar = document.querySelector('.progress-bar-fill');
  if (bar) {
    const targetWidth = bar.style.width;
    bar.style.width = '0%';
    setTimeout(function () { bar.style.width = targetWidth; }, 100);
  }


  // ── Subtle row hover highlight for completed rows ────────────────────────
  const completedRows = document.querySelectorAll('.row--completed');
  completedRows.forEach(function (row) {
    row.title = 'Task completed';
  });

});
// DARK MODE
const toggleBtn = document.getElementById("theme-toggle");

if (toggleBtn) {
    toggleBtn.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("theme", "dark");
        } else {
            localStorage.setItem("theme", "light");
        }
    });
}

// Load saved theme
window.onload = function () {
    if (localStorage.getItem("theme") === "dark") {
        document.body.classList.add("dark-mode");
    }
};
function togglePlan() {
    const plan = document.getElementById("study-plan");
    plan.style.display = (plan.style.display === "none") ? "block" : "none";
}
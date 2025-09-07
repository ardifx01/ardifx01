const fs = require("fs");
const fetch = require("node-fetch");

async function getRepos() {
  const response = await fetch("https://api.github.com/users/ardifx01/repos?sort=updated&per_page=5");
  if (!response.ok) throw new Error("Failed to fetch repos");
  return response.json();
}

function updateReadme(projects) {
  const readme = fs.readFileSync("README.md", "utf-8");
  const lines = readme.split("\n");

  const newLines = [];
  let inside = false;

  for (const line of lines) {
    if (line.includes("<!--START_PROJECTS-->")) {
      newLines.push(line);
      newLines.push(""); // biar ada spasi
      projects.forEach(repo => {
        newLines.push(`- [${repo.name}](${repo.html_url}) ⭐ ${repo.stargazers_count}`);
      });
      inside = true;
    } else if (line.includes("<!--END_PROJECTS-->")) {
      inside = false;
      newLines.push(line);
    } else if (!inside) {
      newLines.push(line);
    }
  }

  fs.writeFileSync("README.md", newLines.join("\n"));
}

(async () => {
  try {
    const repos = await getRepos();
    updateReadme(repos);
    console.log("README updated with latest projects ✅");
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
})();

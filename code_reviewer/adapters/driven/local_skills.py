import os
from code_reviewer.ports.driven import SkillsRepositoryPort

class LocalSkillsRepositoryAdapter(SkillsRepositoryPort):
    def read_all_skills(self) -> str:
        skills_content = []
        
        # Dynamically resolve user home directory config paths
        home_skills_dir = os.path.join(os.path.expanduser("~"), ".gemini", "config", "skills")
        
        paths_to_search = [
            home_skills_dir,
            "../.agents/skills",
            "./.agents/skills"
        ]
        
        for path in paths_to_search:
            if os.path.exists(path) and os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith("SKILL.md") or file.endswith("GEMINI.md") or file.endswith("AGENTS.md"):
                            full_path = os.path.join(root, file)
                            try:
                                with open(full_path, "r", encoding="utf-8") as f:
                                    content = f.read()
                                    skills_content.append(f"### Skill: {file} (Path: {full_path})\n\n{content}\n")
                            except Exception as e:
                                skills_content.append(f"Error reading skill {file}: {str(e)}\n")
                                
        if not skills_content:
            return "No se encontraron skills o directivas de diseño configuradas en las rutas de búsqueda."
            
        return "\n---\n".join(skills_content)

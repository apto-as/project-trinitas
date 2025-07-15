"""
Core component for SuperClaude framework files installation
"""

from typing import Dict, List, Tuple, Any
from pathlib import Path
import json
import shutil

from ..base.component import Component
from ..core.file_manager import FileManager
from ..core.settings_manager import SettingsManager
from ..utils.security import SecurityValidator
from ..utils.logger import get_logger


class CoreComponent(Component):
    """Core SuperClaude framework files component"""
    
    def __init__(self, install_dir: Path = None):
        """Initialize core component"""
        super().__init__(install_dir)
        self.logger = get_logger()
        self.file_manager = FileManager()
        self.settings_manager = SettingsManager(self.install_dir)
        
        # Define framework files to install
        self.framework_files = [
            "CLAUDE.md",
            "COMMANDS.md", 
            "FLAGS.md",
            "PRINCIPLES.md",
            "RULES.md",
            "MCP.md",
            "PERSONAS.md",
            "ORCHESTRATOR.md",
            "MODES.md",
            "Trinitas-base.md"
        ]
        
        # Define Trinitas mode files to install
        self.trinitas_mode_files = [
            "Modes/TRINITAS.md"
        ]
        
        # Define Trinitas commands to install
        self.trinitas_command_files = [
            "trinitas.md"
        ]
    
    def get_metadata(self) -> Dict[str, str]:
        """Get component metadata"""
        return {
            "name": "core",
            "version": "3.0.0",
            "description": "SuperClaude framework documentation and core files",
            "category": "core"
        }
    
    def validate_prerequisites(self) -> Tuple[bool, List[str]]:
        """Check prerequisites for core component"""
        errors = []
        
        # Check if we have read access to source files
        source_dir = self._get_source_dir()
        if not source_dir.exists():
            errors.append(f"Source directory not found: {source_dir}")
            return False, errors
        
        # Check if all required framework files exist
        missing_files = []
        for filename in self.framework_files:
            source_file = source_dir / filename
            if not source_file.exists():
                missing_files.append(filename)
        
        # Check Trinitas mode files
        for filename in self.trinitas_mode_files:
            source_file = source_dir / filename
            if not source_file.exists():
                missing_files.append(filename)
        
        # Check Trinitas command files
        for filename in self.trinitas_command_files:
            source_file = source_dir.parent / "Commands" / filename
            if not source_file.exists():
                missing_files.append(filename)
        
        if missing_files:
            errors.append(f"Missing framework files: {missing_files}")
        
        # Check write permissions to install directory
        has_perms, missing = SecurityValidator.check_permissions(
            self.install_dir, {'write'}
        )
        if not has_perms:
            errors.append(f"No write permissions to {self.install_dir}: {missing}")
        
        # Validate installation target
        is_safe, validation_errors = SecurityValidator.validate_installation_target(self.install_dir)
        if not is_safe:
            errors.extend(validation_errors)
        
        return len(errors) == 0, errors
    
    def get_files_to_install(self) -> List[Tuple[Path, Path]]:
        """Get list of files to install"""
        source_dir = self._get_source_dir()
        files = []
        
        # Add framework files
        for filename in self.framework_files:
            source = source_dir / filename
            target = self.install_dir / filename
            files.append((source, target))
        
        # Add Trinitas mode files
        for filename in self.trinitas_mode_files:
            source = source_dir / filename
            target = self.install_dir / filename
            files.append((source, target))
        
        # Add Trinitas command files
        for filename in self.trinitas_command_files:
            source = source_dir.parent / "Commands" / filename
            target = self.install_dir / "commands" / filename
            files.append((source, target))
        
        return files
    
    def get_metadata_modifications(self) -> Dict[str, Any]:
        """Get metadata modifications for SuperClaude"""
        return {
            "framework": {
                "version": "3.0.0",
                "name": "SuperClaude",
                "description": "AI-enhanced development framework for Claude Code",
                "installation_type": "global",
                "components": ["core"]
            },
            "superclaude": {
                "enabled": True,
                "version": "3.0.0",
                "profile": "default",
                "auto_update": False
            }
        }
    
    def get_settings_modifications(self) -> Dict[str, Any]:
        """Get settings.json modifications (now only Claude Code compatible settings)"""
        # Return empty dict as we don't modify Claude Code settings
        return {}
    
    def install(self, config: Dict[str, Any]) -> bool:
        """Install core component"""
        try:
            self.logger.info("Installing SuperClaude core framework files...")
            
            # Validate installation
            success, errors = self.validate_prerequisites()
            if not success:
                for error in errors:
                    self.logger.error(error)
                return False
            
            # Get files to install
            files_to_install = self.get_files_to_install()
            
            # Validate files for security (split by directory)
            source_dir = self._get_source_dir()
            commands_dir = source_dir.parent / "Commands"
            
            # Split files by source directory
            core_files = []
            command_files = []
            
            for source, target in files_to_install:
                try:
                    # Check if source is in Core directory
                    source.relative_to(source_dir)
                    core_files.append((source, target))
                except ValueError:
                    # Source is in Commands directory
                    command_files.append((source, target))
            
            # Validate core files
            if core_files:
                is_safe, security_errors = SecurityValidator.validate_component_files(
                    core_files, source_dir, self.install_dir
                )
                if not is_safe:
                    for error in security_errors:
                        self.logger.error(f"Security validation failed (core): {error}")
                    return False
            
            # Validate command files
            if command_files:
                is_safe, security_errors = SecurityValidator.validate_component_files(
                    command_files, commands_dir, self.install_dir
                )
                if not is_safe:
                    for error in security_errors:
                        self.logger.error(f"Security validation failed (commands): {error}")
                    return False
            
            # Ensure install directory exists
            if not self.file_manager.ensure_directory(self.install_dir):
                self.logger.error(f"Could not create install directory: {self.install_dir}")
                return False
            
            # Copy framework files
            success_count = 0
            for source, target in files_to_install:
                self.logger.debug(f"Copying {source.name} to {target}")
                
                if self.file_manager.copy_file(source, target):
                    success_count += 1
                    self.logger.debug(f"Successfully copied {source.name}")
                else:
                    self.logger.error(f"Failed to copy {source.name}")
            
            if success_count != len(files_to_install):
                self.logger.error(f"Only {success_count}/{len(files_to_install)} files copied successfully")
                return False
            
            # Create or update metadata
            try:
                metadata_mods = self.get_metadata_modifications()
                # Update metadata directly
                existing_metadata = self.settings_manager.load_metadata()
                merged_metadata = self.settings_manager._deep_merge(existing_metadata, metadata_mods)
                self.settings_manager.save_metadata(merged_metadata)
                self.logger.info("Updated metadata with framework configuration")
                
                # Add component registration to metadata
                self.settings_manager.add_component_registration("core", {
                    "version": "3.0.0",
                    "category": "core",
                    "files_count": len(self.framework_files)
                })
                self.logger.info("Updated metadata with core component registration")
                
                # Migrate any existing SuperClaude data from settings.json
                if self.settings_manager.migrate_superclaude_data():
                    self.logger.info("Migrated existing SuperClaude data from settings.json")
            except Exception as e:
                self.logger.error(f"Failed to update metadata: {e}")
                return False
            
            # Create additional directories for other components and Trinitas mode
            additional_dirs = ["commands", "hooks", "backups", "logs", "Modes"]
            for dirname in additional_dirs:
                dir_path = self.install_dir / dirname
                if not self.file_manager.ensure_directory(dir_path):
                    self.logger.warning(f"Could not create directory: {dir_path}")
            
            # Auto-integrate Trinitas mode into MODES.md if enabled
            if config.get("trinitas_mode", False):
                self._integrate_trinitas_mode()
            
            self.logger.success(f"Core component installed successfully ({success_count} files)")
            return True
            
        except Exception as e:
            self.logger.exception(f"Unexpected error during core installation: {e}")
            return False
    
    def uninstall(self) -> bool:
        """Uninstall core component"""
        try:
            self.logger.info("Uninstalling SuperClaude core component...")
            
            # Remove framework files
            removed_count = 0
            all_files = self.framework_files + self.trinitas_mode_files + self.trinitas_command_files + self.trinitas_command_files
            for filename in all_files:
                file_path = self.install_dir / filename
                if self.file_manager.remove_file(file_path):
                    removed_count += 1
                    self.logger.debug(f"Removed {filename}")
                else:
                    self.logger.warning(f"Could not remove {filename}")
            
            # Update metadata to remove core component
            try:
                if self.settings_manager.is_component_installed("core"):
                    self.settings_manager.remove_component_registration("core")
                    self.logger.info("Removed core component from metadata")
            except Exception as e:
                self.logger.warning(f"Could not update metadata: {e}")
            
            self.logger.success(f"Core component uninstalled ({removed_count} files removed)")
            return True
            
        except Exception as e:
            self.logger.exception(f"Unexpected error during core uninstallation: {e}")
            return False
    
    def get_dependencies(self) -> List[str]:
        """Get component dependencies (core has none)"""
        return []
    
    def update(self, config: Dict[str, Any]) -> bool:
        """Update core component"""
        try:
            self.logger.info("Updating SuperClaude core component...")
            
            # Check current version
            current_version = self.settings_manager.get_component_version("core")
            target_version = self.get_metadata()["version"]
            
            if current_version == target_version:
                self.logger.info(f"Core component already at version {target_version}")
                return True
            
            self.logger.info(f"Updating core component from {current_version} to {target_version}")
            
            # Create backup of existing files
            backup_files = []
            all_files = self.framework_files + self.trinitas_mode_files + self.trinitas_command_files + self.trinitas_command_files
            for filename in all_files:
                file_path = self.install_dir / filename
                if file_path.exists():
                    backup_path = self.file_manager.backup_file(file_path)
                    if backup_path:
                        backup_files.append(backup_path)
                        self.logger.debug(f"Backed up {filename}")
            
            # Perform installation (overwrites existing files)
            success = self.install(config)
            
            if success:
                # Remove backup files on successful update
                for backup_path in backup_files:
                    try:
                        backup_path.unlink()
                    except Exception:
                        pass  # Ignore cleanup errors
                
                self.logger.success(f"Core component updated to version {target_version}")
            else:
                # Restore from backup on failure
                self.logger.warning("Update failed, restoring from backup...")
                for backup_path in backup_files:
                    try:
                        original_path = backup_path.with_suffix('')
                        shutil.move(str(backup_path), str(original_path))
                        self.logger.debug(f"Restored {original_path.name}")
                    except Exception as e:
                        self.logger.error(f"Could not restore {backup_path}: {e}")
            
            return success
            
        except Exception as e:
            self.logger.exception(f"Unexpected error during core update: {e}")
            return False
    
    def validate_installation(self) -> Tuple[bool, List[str]]:
        """Validate core component installation"""
        errors = []
        
        # Check if all framework files exist
        all_files = self.framework_files + self.trinitas_mode_files + self.trinitas_command_files
        for filename in all_files:
            file_path = self.install_dir / filename
            if not file_path.exists():
                errors.append(f"Missing framework file: {filename}")
            elif not file_path.is_file():
                errors.append(f"Framework file is not a regular file: {filename}")
        
        # Check metadata registration
        if not self.settings_manager.is_component_installed("core"):
            errors.append("Core component not registered in metadata")
        else:
            # Check version matches
            installed_version = self.settings_manager.get_component_version("core")
            expected_version = self.get_metadata()["version"]
            if installed_version != expected_version:
                errors.append(f"Version mismatch: installed {installed_version}, expected {expected_version}")
        
        # Check metadata structure
        try:
            framework_config = self.settings_manager.get_metadata_setting("framework")
            if not framework_config:
                errors.append("Missing framework configuration in metadata")
            else:
                required_keys = ["version", "name", "description"]
                for key in required_keys:
                    if key not in framework_config:
                        errors.append(f"Missing framework.{key} in metadata")
        except Exception as e:
            errors.append(f"Could not validate metadata: {e}")
        
        return len(errors) == 0, errors
    
    def _get_source_dir(self) -> Path:
        """Get source directory for framework files"""
        # Assume we're in SuperClaude/setup/components/core.py
        # and framework files are in SuperClaude/SuperClaude/Core/
        project_root = Path(__file__).parent.parent.parent
        return project_root / "SuperClaude" / "Core"
    
    def get_size_estimate(self) -> int:
        """Get estimated installation size"""
        total_size = 0
        source_dir = self._get_source_dir()
        
        # Calculate size for framework files
        for filename in self.framework_files:
            file_path = source_dir / filename
            if file_path.exists():
                total_size += file_path.stat().st_size
        
        # Calculate size for Trinitas mode files
        for filename in self.trinitas_mode_files:
            file_path = source_dir / filename
            if file_path.exists():
                total_size += file_path.stat().st_size
        
        # Calculate size for Trinitas command files
        for filename in self.trinitas_command_files:
            file_path = source_dir.parent / "Commands" / filename
            if file_path.exists():
                total_size += file_path.stat().st_size
        
        # Add overhead for settings.json and directories
        total_size += 15360  # ~15KB overhead (increased for Trinitas files)
        
        return total_size
    
    def get_installation_summary(self) -> Dict[str, Any]:
        """Get installation summary"""
        total_files = len(self.framework_files) + len(self.trinitas_mode_files) + len(self.trinitas_command_files)
        return {
            "component": self.get_metadata()["name"],
            "version": self.get_metadata()["version"],
            "files_installed": total_files,
            "framework_files": self.framework_files,
            "trinitas_mode_files": self.trinitas_mode_files,
            "trinitas_command_files": self.trinitas_command_files,
            "estimated_size": self.get_size_estimate(),
            "install_directory": str(self.install_dir),
            "dependencies": self.get_dependencies(),
            "trinitas_enabled": True
        }
    
    def _integrate_trinitas_mode(self) -> None:
        """Integrate Trinitas mode into MODES.md file"""
        try:
            modes_file = self.install_dir / "MODES.md"
            if not modes_file.exists():
                self.logger.warning("MODES.md file not found for Trinitas integration")
                return
            
            # Read current content
            content = modes_file.read_text(encoding='utf-8')
            
            # Check if Trinitas is already integrated
            if "Trinitas Meta-Persona" in content and "@Modes/TRINITAS.md" in content:
                self.logger.info("Trinitas mode already integrated in MODES.md")
                return
            
            # Add Trinitas to overview section
            if "Three primary modes for optimal performance:" in content:
                content = content.replace(
                    "Three primary modes for optimal performance:",
                    "Four primary modes for optimal performance:"
                )
                content = content.replace(
                    "3. **Token Efficiency**: Optimized communication and resource management",
                    "3. **Token Efficiency**: Optimized communication and resource management\n4. **Trinitas Meta-Persona**: Multi-perspective analysis and strategic coordination"
                )
            
            # Add Trinitas mode section at the end
            if not content.endswith("\n"):
                content += "\n"
            
            content += "\n---\n\n# Trinitas Meta-Persona Mode\n\n@Modes/TRINITAS.md\n"
            
            # Write updated content
            modes_file.write_text(content, encoding='utf-8')
            self.logger.success("Successfully integrated Trinitas mode into MODES.md")
            
        except Exception as e:
            self.logger.error(f"Failed to integrate Trinitas mode into MODES.md: {e}")
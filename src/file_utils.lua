local M = {}

function M.openFiles()
	love.window.showFileDialog("openfile", function(files, filtername, errorstring)
		if errorstring then
			print(errorstring)
			return
		end
		if files then
			for _, file in pairs(files) do
				print(file)
			end
		end
	end, {
		multiselect = true,
		acceptlabel = "Annotate",
		filters = { PNG = "png" },
	})
end

return M
